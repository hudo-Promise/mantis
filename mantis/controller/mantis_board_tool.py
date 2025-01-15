# -*- coding: utf-8 -*-
import json

from common_tools.tools import create_current_format_time, generate_uuid, op11_redis_client
from mantis.controller.mantis_card_tool import delete_card_func, query_card_func, create_card_func
from mantis.controller.mantis_milestone_tool import delete_milestone_by_id, query_milestone, create_milestone
from mantis.models import mantis_db
from mantis.models.boards import Board, MileStone, Card, BoardLocation
from mantis.models.mantis_config import MantisMappingRule


def create_board(request_params):
    user_id = request_params.get('user_id')
    name = request_params.get('name')
    description = request_params.get('desc', '')
    cluster = request_params.get('cluster')
    visibility_level = request_params.get('visibility_level', 0)
    if not name:
        return 10004, None
    board = Board(
        board_id=generate_uuid(),
        user_id=user_id,
        username=json.loads(op11_redis_client.get('tms_user_info')).get(str(user_id)).get('username').lower(),
        name=name,
        description=description if description else '',
        cluster=cluster,
        status=0,
        create_time=create_current_format_time(),
        visibility_level=visibility_level,
        delete_flag=0,
    )
    mantis_db.session.add(board)
    mantis_db.session.flush()
    dashboard_unique_id = board.board_id
    try:
        mantis_db.session.commit()
    except Exception as e:
        print(e)
        mantis_db.session.rollback()
        return 10008, None
    return 200, dashboard_unique_id


def edit_board_tool(request_params):
    if not request_params.get('name'):
        return 10004
    board = Board.query.filter(Board.id == request_params.get('board_id')).first()
    board.name = request_params.get('name')
    board.description = request_params.get('desc', '')
    board.status = request_params.get('status')

    board.visibility_level = request_params.get('visibility_level', 0)
    mantis_db.session.commit()
    return 200


def delete_board_func(request_params):
    board_id = request_params.get('board_id')
    user_id = request_params.get('user_id')
    try:
        # delete board
        Board.query.filter(Board.board_id == board_id, Board.user_id == user_id).delete()
        # delete milestone
        ms = MileStone.query.filter(MileStone.board_id == board_id).all()
        milestone_id_list = []
        for item in ms:
            milestone_id_list.append(item.id)
        delete_milestone_by_id(milestone_id_list)
        # delete card
        cards = Card.query.filter(Card.board_id == board_id).all()
        card_id_list = []
        for card in cards:
            card_id_list.append(card.id)
        delete_card_func(card_id_list)
        BoardLocation.query.filter(BoardLocation.board_id == board_id).delete()
        mantis_db.session.commit()
        return 200
    except Exception as e:
        print(e)
        mantis_db.session.rollback()
        return 500


def get_board_func(request_params):
    query_type = request_params.get('query_type')
    page_num = request_params.get('page_num')
    page_size = request_params.get('page_size')

    user_id = request_params.get('user_id')
    board_id = request_params.get('board_id')
    cluster = request_params.get('cluster')

    username = request_params.get('username')
    dashboard_name = request_params.get('dashboard_name')

    query_filter_dict = {
        'private': [Board.user_id == user_id, Board.delete_flag == 0],
        'public': [Board.visibility_level == 1, Board.delete_flag == 0],
        'precise': [Board.visibility_level == 1, Board.delete_flag == 0],
        'recommend': [Board.visibility_level == 1]
    }
    if query_type == 'precise':
        if board_id:
            query_filter_dict['precise'].append(Board.id == int(board_id))
        if user_id:
            query_filter_dict['precise'].append(Board.user_id == user_id)
    if username:
        query_filter_dict['public'].append(Board.username.like('%' + username.lower() + '%'))
    if dashboard_name:
        query_filter_dict['public'].append(Board.name.like('%' + dashboard_name + '%'))
    if cluster:
        query_filter_dict[query_type].append(Board.cluster == cluster)

    query_filter = query_filter_dict.get(query_type)
    total_num = None
    if page_size and page_num:
        if query_type == 'recommend':
            board_data = Board.query.filter(
                *query_filter
            ).order_by(Board.create_time.desc()).limit(page_size).offset((page_num - 1) * page_size).all()
        else:
            board_data = Board.query.filter(*query_filter).limit(page_size).offset((page_num - 1) * page_size).all()
        total_num = len(Board.query.filter(*query_filter).all())
    else:
        board_data = Board.query.filter(*query_filter).all()
    data = []
    dashboard = get_dashboard_content()

    mapping_rule = mantis_db.session.query(MantisMappingRule.id, MantisMappingRule.cluster_id).all()
    cluster2mapping_rule = {rule.cluster_id: rule.id for rule in mapping_rule}
    for item in board_data:
        current_dashboard = {
            'id': item.id,
            'user_id': item.user_id,
            'username': item.username.title(),
            'board_uuid': item.board_id,
            'name': item.name,
            'desc': item.description,
            'cluster': item.cluster,
            'mapping_rule': cluster2mapping_rule.get(item.cluster),
            'status': item.status,
            'visibility_level': item.visibility_level,
            'create_time': str(item.create_time)
        }
        if dashboard.get(item.board_id):
            current_dashboard['card_name'] = dashboard.get(item.board_id).get('card_name').strip(',').strip()
            current_dashboard['card_count'] = dashboard.get(item.board_id).get('card_count')
        else:
            current_dashboard['card_name'] = None
            current_dashboard['card_count'] = 0
        data.append(current_dashboard)
    result = {
       'data': data,
       'total_num': total_num
    }
    return result


def get_dashboard_content():
    milestones = MileStone.query.filter().all()
    cards = Card.query.filter().all()
    dashboard = {}
    for milestone in milestones:
        generate_dashboard_content(dashboard, milestone, 'milestone')
    for card in cards:
        generate_dashboard_content(dashboard, card, 'card')
    return dashboard


def generate_dashboard_content(dashboard, card, mode):
    if card.board_id not in dashboard:
        dashboard[card.board_id] = {
            'card_name': '',
            'card_count': 0
        }
    card_name = card.milestone_name if mode == 'milestone' else card.name
    dashboard[card.board_id]['card_name'] += ', ' + card_name
    dashboard[card.board_id]['card_count'] += 1


def create_board_location_func(request_params):
    bl = BoardLocation(
        board_id=request_params.get('board_id'),
        location_id=request_params.get('location_id'),
        type=request_params.get('type'),
        length=request_params.get('length'),
        width=request_params.get('width'),
        data_id=request_params.get('data_id')
    )
    mantis_db.session.add(bl)
    mantis_db.session.commit()


def update_board_location_func(request_params):
    """
    {"board_id": xx,
    "source_location_id": xx,
    "target_location_id": xx,
    'type': xx, 'length': xx, 'width': xx, 'action': 'edit/delete/move'}
    """
    if request_params.get('action') == 'edit':
        BoardLocation.query.filter(
            BoardLocation.board_id == request_params.get('board_id'),
            BoardLocation.data_id == request_params.get('data_id'),
            BoardLocation.type == request_params.get('type')
        ).update({'length': request_params.get('length'), 'width': request_params.get('width')})
    board_locations = BoardLocation.query.filter(
        BoardLocation.board_id == request_params.get('board_id')
    ).order_by(BoardLocation.location_id).all()
    location_flag = 0
    if request_params.get('action') == 'delete':
        delete_dict = {'milestone': delete_milestone_by_id, 'card': delete_card_func}
        for location in board_locations:
            if location.location_id == request_params.get('source_location_id'):
                delete_dict.get(location.type)([location.data_id])
                BoardLocation.query.filter(
                    BoardLocation.data_id == request_params.get('data_id'),
                    BoardLocation.type == request_params.get('type')
                ).delete()
            else:
                location.location_id = location_flag
                location_flag += 1

    if request_params.get('action') == 'move':
        board_locations.insert(
            request_params.get('target_location_id'),
            board_locations.pop(request_params.get('source_location_id')))
        for location in board_locations:
            location.location_id = location_flag
            location_flag += 1
    mantis_db.session.commit()


def get_board_data_func(request_params):
    board_id = request_params.get('board_id')
    board = Board.query.filter(Board.board_id == board_id).first()
    title = board.name
    bls = BoardLocation.query.filter(BoardLocation.board_id == board_id).all()
    milestone_data = query_milestone({'board_id': board_id})
    card_data = query_card_func({'board_id': board_id})
    result = []
    for bl in bls:
        result.append({
            'board_id': bl.board_id,
            'location_id': bl.location_id,
            'type': bl.type,
            'length': bl.length,
            'width': bl.width,
            'data_id': bl.data_id,
            'data': milestone_data.get(bl.data_id, None) if bl.type == 'milestone' else card_data.get(bl.data_id, None),
        })
    result.sort(key=lambda r: r['location_id'])
    board_info = {
        'dashboard_data': result,
        'dashboard_title': title
    }
    return board_info


def clone_dashboard_tool(request_params):
    clone_type = request_params.get('clone_type')
    cluster = request_params.get('cluster')
    config = request_params.get('config')
    target_dict = {
        'create': request_params.get('target_user_id'),
        'insert': request_params.get('target_dashboard_id')
    }
    target_id = target_dict.get(clone_type)
    if clone_type == 'create':
        user_id = target_id
        create_params = {
            'user_id': user_id,
            'name': request_params.get('name'),
            'desc': request_params.get('desc'),
            'cluster': str(cluster),
            'visibility_level': request_params.get('visibility_level', 0),
        }
        code, dashboard_unique_id = create_board(create_params)
    elif clone_type == 'insert':
        dashboard_unique_id = target_id
    else:
        dashboard_unique_id = None
    milestone_list, card_list = params_clone_config(config, dashboard_unique_id, cluster)
    create_milestone_and_card_dashboard(dashboard_unique_id, milestone_list, card_list, clone_type)


def params_clone_config(config, dashboard_unique_id, cluster):
    milestone_ids = config.get('milestone_id')
    card_ids = config.get('card_id')
    milestone_list = query_clone_milestone_config(milestone_ids, dashboard_unique_id, cluster)
    card_list = query_clone_card_config(card_ids, dashboard_unique_id, cluster)
    return milestone_list, card_list


def query_clone_milestone_config(milestone_ids, dashboard_unique_id, cluster):
    mss = MileStone.query.filter(MileStone.id.in_(milestone_ids)).all()
    milestone_list = []
    for ms in mss:
        current_milestone = {
            'milestone_name': ms.milestone_name,
            'cluster': [str(cluster)],
            'board_id': dashboard_unique_id,
            'category': ms.category,
            'available_market': ms.available_market,
            'available_platform': ms.available_platform,
            'available_carline': ms.available_carline,
            'available_language': ms.available_language,
            'available_environment': ms.available_environment,
            'available_variant': ms.available_variant,
            'start_date': ms.start_date,
            'end_date': ms.end_date,
            'start_year': ms.start_year,
            'end_year': ms.end_year,
            'start_week': ms.start_week,
            'end_week': ms.end_week,
            'milestone_line': ms.milestone_line,
            'milestone_group': ms.milestone_group,
            'create_time': create_current_format_time(),
            'delete_flag': ms.delete_flag,
        }
        generate_logic_func(current_milestone, ms.available_logic)
        milestone_list.append(current_milestone)
    return milestone_list


def query_clone_card_config(milestone_ids, dashboard_unique_id, cluster):
    cs = Card.query.filter(Card.id.in_(milestone_ids)).all()
    card_list = []
    for c in cs:
        current_card = {
            'name': c.name,
            'bar_type': c.bar_type,
            'cluster': [str(cluster)],
            'board_id': dashboard_unique_id,
            'category': c.category,
            'available_market': c.available_market,
            'test_market': c.test_market,
            'available_platform': c.available_platform,
            'test_platform': c.test_platform,
            'available_carline': c.available_carline,
            'test_carline': c.test_carline,
            'available_language': c.available_language,
            'test_language': c.test_language,
            'available_environment': c.available_environment,
            'test_environment': c.test_environment,
            'available_variant': c.available_variant,
            'test_variant': c.test_variant,
            'level': c.level,
            'card_groups': c.card_groups,
        }
        generate_logic_func(current_card, c.available_logic)
        card_list.append(current_card)
    return card_list


def create_milestone_and_card_dashboard(board_id, milestone_list, card_list, operation):
    if operation == 'create':
        location_id = 0
    else:
        location_id = len(BoardLocation.query.filter(BoardLocation.board_id == board_id).all())
    for milestone in milestone_list:
        _, milestone_id = create_milestone(milestone)
        generate_location_params(board_id, location_id, 'milestone', milestone_id)
        location_id += 1
    for card in card_list:
        _, card_id = create_card_func(card)
        generate_location_params(board_id, location_id, 'card', card_id)
        location_id += 1


def generate_location_params(board_id, location_id, card_type, data_id):
    location_params = {
        'board_id': board_id,
        'location_id': location_id,
        'type': card_type,
        'length': 300,
        'width': 500,
        'data_id': data_id
    }
    create_board_location_func(location_params)


def generate_logic_func(current_graph, available_logic):
    for key, value in available_logic.items():
        current_graph[f'{key}_logic'] = value
