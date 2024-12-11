from operator import or_

from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from common_tools.tools import create_current_format_time, update_tool, get_gap_days, calculate_time_to_finish, \
    conditional_filter
from mantis.controller.mantis_test_milestone_tool import get_test_milestone_by_id, parse_case_filter_config, \
    get_case_current_result
from mantis.models import mantis_db
from mantis.models.case import TestCase, CaseResult, MantisFilterRecord
from mantis.models.mantis_test_milestone_cycle import MantisTestCycle


def mantis_create_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    mtc = MantisTestCycle(
        name=request_params.get('name'),
        test_group=request_params.get('test_group'),
        linked_milestone=request_params.get('linked_milestone'),
        project=milestone.project,
        cluster=milestone.cluster,
        market=request_params.get('market'),
        start_date=request_params.get('start_date'),
        due_date=request_params.get('due_date'),
        description=request_params.get('description'),
        filter_id=request_params.get('filter_id'),
        test_scenario=request_params.get('test_scenario'),
        free_test_item=request_params.get('free_test_item'),
        status=1,
        create_time=current_time,
        update_time=current_time,
    )
    mantis_db.session.add(mtc)
    mantis_db.session.commit()


def mantis_edit_test_cycle_tool(request_params):
    mtc = MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).first()
    update_dict = {'update_time': create_current_format_time()}
    update_key = [
        'name', 'test_group', 'linked_milestone', 'market', 'start_date', 'due_date', 'description', 'filter_id',
        'test_scenario', 'free_test_item', 'status'
    ]
    update_tool(update_dict, request_params, update_key, mtc)
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    update_dict['cluster'] = milestone.cluster
    update_dict['project'] = milestone.project
    MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).update(update_dict)
    mantis_db.session.commit()


def mantis_get_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    mtc_list = MantisTestCycle.query.filter(MantisTestCycle.cluster == request_params.get('cluster')).all()
    return list(map(lambda mtc: generate_test_cycle_tool(current_time, mtc), mtc_list))


def generate_test_cycle_tool(current_time, mtc):
    return {
        'id': mtc.id,
        'name': mtc.name,
        'test_group': mtc.test_group,
        'linked_milestone': mtc.linked_milestone,
        'project': mtc.project,
        'cluster': mtc.cluster,
        'market': mtc.market,
        'start_date': mtc.start_date,
        'due_date': mtc.due_date,
        'actual_finish_date': mtc.actual_finish_date,
        'description': mtc.description,
        'filter_id': mtc.filter_id,
        'test_scenario': mtc.test_scenario,
        'free_test_item': mtc.free_test_item,
        'status': mtc.status,
        'time_left': get_gap_days(current_time, f'{mtc.due_date} 00:00:00') + 1,
        'time_to_finish': calculate_time_to_finish(
            get_gap_days(f'{mtc.start_date} 00:00:00', current_time) + 1,
            0.9
        ),  # TODO
        'create_time': str(mtc.create_time),
        'update_time': str(mtc.update_time),
    }


def mantis_delete_test_cycle_tool(request_params):
    MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).delete()
    mantis_db.session.commit()


def mantis_get_test_cycle_insight_graph_tool(params_dict):
    mtc = get_test_cycle_join_filter_record(params_dict.get('id'))
    ret = get_case_current_result(mtc.filter_config, query_type=params_dict.get('query_type'))
    return ret


def mantis_get_test_cycle_burnout_diagram_tool(params_dict):
    # TODO
    mtc = get_test_cycle_join_filter_record(params_dict.get('id'))
    ret = get_case_current_result(mtc.filter_config, query_type=params_dict.get('query_type'))
    return ret


def get_test_cycle_join_filter_record(cycle_id):
    filter_list = [MantisTestCycle.id == cycle_id]
    query_list = [MantisTestCycle.test_scenario, MantisFilterRecord.filter_config]
    mtc = mantis_db.session.query(*query_list).json(
        MantisFilterRecord, MantisTestCycle.filter_id == MantisFilterRecord.id, isouter=True
    ).filter(*filter_list).first()
    return mtc
