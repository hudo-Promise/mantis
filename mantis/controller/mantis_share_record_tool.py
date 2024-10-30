# -*- coding: utf-8 -*-
import copy
import json

from common_tools.tools import (
    create_current_format_time, generate_uuid, calculate_full_day_between_two_dates, op11_redis_client
)
from config.mantis_setting import mantis_share_url_prefix
from email_service.mantis_eamil_service import async_send_mantis_email
from mantis.controller.mantis_card_tool import query_card_func
from mantis.controller.mantis_milestone_tool import query_milestone
from mantis.models import mantis_db
from mantis.models.boards import Board, Card, MileStone
from mantis.models.mantis_share_record import MantisShareRecord


def create_share_record_tool(request_params):
    """
        content: dict
            {
                sender_name:
                dashboard_name:
                share_time:
                url:
                data: [
                    {id: card_name: type: cluster:}
                ]
            }
        config: dict
            {
                dashboard_id: {
                    card_id: [1, 2, 3]
                    milestone_id: [4, 5]
                }
            }
    """
    share_type = request_params.get('share_type')
    sender = request_params.get('sender')
    config = request_params.get('config')
    create_time = create_current_format_time()
    receivers = request_params.get('receiver')
    if not receivers:
        if share_type == 2:
            share_key = request_params.get('share_key')
            if share_key != "000000":
                return 10002, None
        receivers = []
        for user_id in json.loads(op11_redis_client.get('tms_user_info')).keys():
            receivers.append(int(user_id))
    result = None
    if share_type == 1:  # station_mail
        content = generate_share_record_content(sender, config, create_time)
        for receiver in receivers:
            if int(receiver) == int(sender):
                continue
            unique_id = generate_uuid()
            current_content = copy.deepcopy(content)
            current_content['url'] = mantis_share_url_prefix % unique_id
            add_share_record(
                create_time, unique_id, sender, config, share_type, content=current_content, receiver=[receiver]
            )
    elif share_type == 2:  # e_mail
        unique_id = generate_uuid()
        add_share_record(create_time, unique_id, sender, config, share_type, content=None, receiver=receivers)
        content = generate_share_record_content(sender, config, create_time)
        content['url'] = mantis_share_url_prefix % unique_id
        content['receivers'] = receivers
        async_send_mantis_email(content)
    elif share_type == 3:  # url
        unique_id = generate_uuid()
        receivers.append(sender)
        add_share_record(create_time, unique_id, sender, config, share_type, receiver=receivers)
        result = mantis_share_url_prefix % unique_id
    mantis_db.session.commit()
    return 200, result


def generate_share_record_content(sender, config, create_time):
    dashboard = []
    milestones = []
    cards = []
    for key, value in config.items():
        dashboard.append(key)
        milestones += value.get('milestone_id')
        cards += value.get('card_id')
    dashboard_name, data_list = query_share_dashboard(dashboard, milestones, cards)
    user_info = json.loads(op11_redis_client.get('tms_user_info'))
    content = {
        'sender_name': user_info.get(str(sender)),
        'dashboard_name': ','.join(dashboard_name),
        'share_time': str(create_time),
        'data': data_list
    }
    return content


def query_share_dashboard(dashboard, milestones, cards):
    dashboard_name = []
    if dashboard:
        boards = Board.query.filter(Board.board_id.in_(dashboard)).all()
        for board in boards:
            dashboard_name.append(board.name)
    data_list = []
    if milestones:
        mss = MileStone.query.filter(MileStone.id.in_(milestones)).all()
        for ms in mss:
            data_list.append(
                {'id': ms.id, 'card_name': ms.milestone_name, 'type': 'milestone', 'cluster': ms.cluster[0]}
            )
    if cards:
        cs = Card.query.filter(Card.id.in_(cards)).all()
        for c in cs:
            data_list.append(
                {'id': c.id, 'card_name': c.name, 'type': 'card', 'cluster': c.cluster[0]}
            )
    return dashboard_name, data_list


def add_share_record(create_time, unique_id, sender, config, share_type, content=None, receiver=None):
    msm = MantisShareRecord(
        unique_id=unique_id,
        sender=sender,
        share_type=share_type,
        receiver=receiver,
        status=1,
        content=content,
        config=config,
        create_time=create_time,
        update_time=create_time,
        delete_flag=0
    )
    mantis_db.session.add(msm)


def mark_station_mail_tool(request_params):
    user_id = request_params.get('user_id')
    share_record_id = request_params.get('share_record_id')
    update_time = create_current_format_time()
    if user_id:
        mantis_db.session.query(MantisShareRecord).filter(
            MantisShareRecord.share_type == 1,
            mantis_db.func.json_contains(MantisShareRecord.receiver, json.dumps([user_id]))
        ).update({MantisShareRecord.status: 2, MantisShareRecord.update_time: update_time}, synchronize_session=False)
    else:
        msm = MantisShareRecord.query.filter(MantisShareRecord.id == share_record_id).first()
        msm.status = 2
        msm.update_time = update_time
    mantis_db.session.commit()


def delete_station_mail_tool(request_params):
    share_record_id = request_params.get('share_record_id')
    msr = MantisShareRecord.query.filter(MantisShareRecord.id == share_record_id).first()
    msr.delete_flag = 1
    mantis_db.session.commit()


def query_station_mail_tool(request_params):
    user_id = request_params.get('user_id')
    status = request_params.get('status')
    msm_list = MantisShareRecord.query.filter(
        MantisShareRecord.share_type == 1,
        mantis_db.func.json_contains(MantisShareRecord.receiver, json.dumps(user_id)),
        MantisShareRecord.status.in_(status), MantisShareRecord.delete_flag == 0
    ).order_by(MantisShareRecord.create_time.desc()).all()
    user_info = json.loads(op11_redis_client.get('tms_user_info'))
    msm_result = []
    read = 0
    unread = 0
    current_time = create_current_format_time()
    for msm in msm_list:
        if current_time[0: 10] == str(msm.create_time)[0: 10]:
            display_time = str(msm.create_time)[11:16]
        else:
            days = calculate_full_day_between_two_dates(msm.create_time, current_time) + 1
            if days == 1:
                format_str = '%d day ago'
            else:
                format_str = '%d days ago'
            display_time = format_str % days
        current_msm = {
            'id': msm.id,
            'unique_id': msm.unique_id,
            'sender': msm.sender,
            'sender_name': user_info.get(str(msm.sender)).get('username'),
            'receiver': msm.receiver,
            'receiver_name': user_info.get(str(msm.receiver[0])).get('username'),
            'status': msm.status,
            'content': msm.content,
            'create_time': str(msm.create_time),
            'display_time': display_time
        }
        msm_result.append(current_msm)
        if msm.status == 1:
            unread += 1
        elif msm.status == 2:
            read += 1
    result = {
        'station_mail': msm_result,
        'read': read,
        'unread': unread
    }
    return result


def query_share_detail_by_url(request_params):
    unique_id = request_params.get('unique_id')
    user_id = request_params.get('user_id')
    msr = MantisShareRecord.query.filter(MantisShareRecord.unique_id == unique_id).first()
    if msr.receiver is not None:
        if int(user_id) not in msr.receiver:
            return 404, None
    return process_share_detail(msr.config, msr.sender)


def batch_query_public_detail(request_params):
    unique_id_list = request_params.get('unique_id_list')
    config_dict = {}
    for unique_id in unique_id_list:
        config_dict[unique_id] = None
    code, result = process_share_detail(config_dict)
    return code, result.get('milestone') + result.get('card')


def process_share_detail(share_config, sender=None):
    milestone_list = []
    card_list = []
    location_id = 0
    for dashboard_id, dashboard_config in share_config.items():
        milestone_data = query_milestone({'board_id': dashboard_id})
        location_id = generate_share_detail(
            dashboard_id, milestone_data, dashboard_config, milestone_list, location_id, 'milestone'
        )
        card_data = query_card_func({'board_id': dashboard_id})
        location_id = generate_share_detail(
            dashboard_id, card_data, dashboard_config, card_list, location_id, 'card'
        )
    result = {
        'milestone': milestone_list,
        'card': card_list
    }
    if sender:
        result['sender'] = json.loads(op11_redis_client.get('tms_user_info')).get(str(sender)).get('username')
    return 200, result


def generate_share_detail(dashboard_id, source_data, dashboard_config, result_list, location_id, mode):
    for data_id, data_dict in source_data.items():
        if not dashboard_config or data_id in dashboard_config.get(mode + '_id'):
            result_list.append({
                'board_id': dashboard_id,
                'location_id': location_id,
                'type': mode,
                'length': 300,
                'width': 500,
                'data_id': data_id,
                'data': data_dict,
            })
            location_id += 1
    return location_id

