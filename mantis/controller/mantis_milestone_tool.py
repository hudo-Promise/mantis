# -*- coding: utf-8 -*-
from common_tools.async_api_tool import update_mantis_single_graph
from mantis.mantis_tool import query_group
from mantis.models import mantis_db
from mantis.models.boards import MileStone, MileStoneGroup, BoardLocation, CardGroup
from common_tools.tools import generate_week, generate_year, create_current_format_time, generate_uuid


def create_milestone(request_params):
    start_date = request_params.get('start_date')
    end_date = request_params.get('end_date')
    """
    {
        'name': {'date': xxxx-xx-xx},
    }
    {
        'name': {
            'date': xxxx-xx-xx, 
            'year': 0, 
            'week': 0
        },
    }
    """
    milestone_line = request_params.get('milestone_line')
    """
    {
        'name': {'start_date': xxxx-xx-xx, 'end_date': xxxx-xx-xx, 'function': []},
    }
    {
        'name': {
            'start_date': xxxx-xx-xx, 
            'end_date': xxxx-xx-xx, 
            'function': [], 
            'start_year': 0, 
            'end_year': 0, 
            'start_week': 0, 
            'end_week': 0
            'result': {}
        },
    }
    """
    milestone_group = request_params.get('milestone_group')
    for milestone_key, milestone_value in milestone_line.items():
        milestone_line[milestone_key]['year'] = generate_year(milestone_value['date'])
        milestone_line[milestone_key]['week'] = generate_week(milestone_value['date'])
    for group_key, group_value in milestone_group.items():
        milestone_group[group_key]['start_year'] = generate_year(group_value['start_date'])
        milestone_group[group_key]['end_year'] = generate_year(group_value['end_date'])
        milestone_group[group_key]['start_week'] = generate_week(group_value['start_date'])
        milestone_group[group_key]['end_week'] = generate_week(group_value['end_date'])
    milestone = MileStone(
        milestone_name=request_params.get('milestone_name'),
        cluster=request_params.get('cluster'),
        board_id=request_params.get('board_id'),
        category=request_params.get('category'),
        available_market=request_params.get('available_market'),
        available_platform=request_params.get('available_platform'),
        available_carline=request_params.get('available_carline'),
        available_variant=request_params.get('available_variant'),
        available_environment=request_params.get('available_environment'),
        available_language=request_params.get('available_language'),
        available_logic={
            'available_carline': request_params.get('available_carline_logic', 'or'),
            'available_variant': request_params.get('available_variant_logic', 'or'),
            'available_market': request_params.get('available_market_logic', 'or'),
            'available_language': request_params.get('available_language_logic', 'or'),
            'available_environment': request_params.get('available_environment_logic', 'or'),
            'available_platform': request_params.get('available_platform_logic', 'or'),
        },
        start_date=start_date,
        end_date=end_date,
        start_year=generate_year(start_date),
        end_year=generate_year(end_date),
        start_week=generate_week(start_date),
        end_week=generate_week(end_date),
        milestone_line=milestone_line,
        milestone_group=milestone_group,
        create_time=create_current_format_time(),
        delete_flag=0
    )
    mantis_db.session.add(milestone)
    mantis_db.session.flush()
    mantis_db.session.commit()
    uuid = generate_uuid()
    update_mantis_single_graph(uuid, milestone.id, 'milestone')
    return uuid, milestone.id


def update_milestone(request_params):
    request_params['start_year'] = generate_year(request_params['start_date'])
    request_params['end_year'] = generate_year(request_params['end_date'])
    request_params['start_week'] = generate_week(request_params['start_date'])
    request_params['end_week'] = generate_week(request_params['end_date'])
    for milestone_key, milestone_value in request_params['milestone_line'].items():
        request_params['milestone_line'][milestone_key]['year'] = generate_year(milestone_value['date'])
        request_params['milestone_line'][milestone_key]['week'] = generate_week(milestone_value['date'])
    for group_key, group_value in request_params['milestone_group'].items():
        request_params['milestone_group'][group_key]['start_year'] = generate_year(group_value['start_date'])
        request_params['milestone_group'][group_key]['end_year'] = generate_year(group_value['end_date'])
        request_params['milestone_group'][group_key]['start_week'] = generate_week(group_value['start_date'])
        request_params['milestone_group'][group_key]['end_week'] = generate_week(group_value['end_date'])
    request_params['available_logic'] = {
        'available_carline': request_params.get('available_carline_logic', 'or'),
        'available_variant': request_params.get('available_variant_logic', 'or'),
        'available_market': request_params.get('available_market_logic', 'or'),
        'available_language': request_params.get('available_language_logic', 'or'),
        'available_environment': request_params.get('available_environment_logic', 'or'),
        'available_platform': request_params.get('available_platform_logic', 'or'),
    }
    milestone_id = request_params['milestone_id']
    del_key_list = [key + '_logic' for key in request_params['available_logic'].keys()]
    del_key_list.append('milestone_id')
    for param_key in del_key_list:
        del request_params[param_key]
    MileStone.query.filter(MileStone.id == milestone_id).update(request_params)
    mantis_db.session.commit()
    uuid = generate_uuid()
    update_mantis_single_graph(uuid, milestone_id, 'milestone')
    return uuid


def query_milestone(request_params):
    board_id = request_params.get('board_id')
    milestone_id = request_params.get('milestone_id', None)
    if milestone_id:
        milestone = MileStone.query.filter(MileStone.id == milestone_id).first()
        msg = query_group(int(milestone_id), 'milestone')
        bl = BoardLocation.query.filter(
            BoardLocation.board_id == board_id,
            BoardLocation.type == 'milestone',
            BoardLocation.data_id == milestone_id
        ).first()
        if bl:
            result = {
                'board_id': bl.board_id,
                'location_id': bl.location_id,
                'type': bl.type,
                'length': bl.length,
                'width': bl.width,
                'data_id': bl.data_id,
                'data': generate_milestone(milestone, msg),
            }
            return result
        else:
            return None
    else:
        milestones = MileStone.query.filter(MileStone.board_id == board_id).all()
        milestone_id = [item.id for item in milestones]
        msg = query_group(milestone_id, 'milestone')
        return {milestone.id: generate_milestone(milestone, msg) for milestone in milestones}


def generate_milestone(milestone, msg):
    milestone_dict = {
        'milestone_id': milestone.id,
        'milestone_name': milestone.milestone_name,
        'cluster': milestone.cluster,
        'board_id': milestone.board_id,
        'category': milestone.category,
        'available_market': milestone.available_market,
        'available_platform': milestone.available_platform,
        'available_carline': milestone.available_carline,
        'available_language': milestone.available_language,
        'available_environment': milestone.available_environment,
        'available_variant': milestone.available_variant,
        'start_date': milestone.start_date,
        'end_date': milestone.end_date,
        'start_year': milestone.start_year,
        'end_year': milestone.end_year,
        'start_week': milestone.start_week,
        'end_week': milestone.end_week,
        'milestone_line': milestone.milestone_line,
        'milestone_group': msg.get(milestone.id),
        'create_time': milestone.create_time,
        'delete_flag': milestone.delete_flag,
        'available_logic': milestone.available_logic
    }
    return milestone_dict


def delete_milestone_by_id(milestone_id):
    MileStone.query.filter(MileStone.id.in_(milestone_id)).delete()
    MileStoneGroup.query.filter(MileStoneGroup.milestone_id.in_(milestone_id)).delete()
    mantis_db.session.commit()


def query_milestone_uuid_status(request_params):
    model_type_dict = {
        'milestone': MileStoneGroup,
        'card': CardGroup
    }
    uuid = request_params.get('update_uuid')
    model_type = request_params.get('type')
    if model_type not in model_type_dict.keys():
        return {'type': 'Invalid', 'id': None}
    record = model_type_dict.get(model_type).query.filter(
        model_type_dict.get(model_type).uuid == uuid).first()
    if record:
        if model_type == 'card':
            record_id = record.card_id
        else:
            record_id = record.milestone_id
    else:
        record_id = None
    result_dict = {
        'type': model_type,
        'id': record_id
    }
    return result_dict
