from collections import Counter

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import aliased

from common_tools.tools import create_current_format_time, get_gap_days, update_tool, calculate_time_to_finish, \
    conditional_filter
from mantis.models import mantis_db
from mantis.models.case import TestCase, CaseResult, MantisFilterRecord
from mantis.models.mantis_test_milestone_cycle import MantisTestMileStone, MantisTestCycle


def mantis_create_test_milestone_tool(request_params):
    current_time = create_current_format_time()
    mtm = MantisTestMileStone(
        name=request_params.get('name'),
        description=request_params.get('description'),
        project=request_params.get('project'),
        cluster=request_params.get('cluster'),
        status=1,
        start_date=request_params.get('start_date'),
        due_date=request_params.get('due_date'),
        create_time=current_time,
        update_time=current_time,
        delete_flag=0
    )
    mantis_db.session.add(mtm)
    mantis_db.session.commit()


def mantis_edit_test_milestone_tool(request_params):
    mtm = MantisTestMileStone.query.filter(MantisTestMileStone.id == request_params.get('id')).first()
    update_dict = {'update_time': create_current_format_time()}
    update_key = ['name', 'description', 'project', 'cluster', 'status', 'due_date']
    update_tool(update_dict, request_params, update_key, mtm)
    MantisTestMileStone.query.filter(MantisTestMileStone.id == request_params.get('id')).update(update_dict)
    mantis_db.session.commit()


def mantis_get_test_milestone_tool(request_params):
    current_time = create_current_format_time()
    mtms = MantisTestMileStone.query.filter(MantisTestMileStone.cluster == request_params.get('cluster')).all()
    return list(map(lambda mtm: generate_test_milestone_tool(current_time, mtm), mtms))


def generate_test_milestone_tool(current_time, mtm):
    return {
        'id': mtm.id,
        'name': mtm.name,
        'description': mtm.description,
        'project': mtm.project,
        'cluster': mtm.cluster,
        'status': mtm.status,
        'start_date': mtm.start_date,
        'due_date': mtm.due_date,
        'time_left': get_gap_days(current_time, f'{mtm.due_date} 00:00:00') + 1,
        'time_to_finish': calculate_time_to_finish(
            get_gap_days(f'{mtm.start_date} 00:00:00', current_time) + 1,
            0.9
        ),  # TODO
        'create_time': str(mtm.create_time),
        'update_time': str(mtm.update_time),
        'delete_flag': mtm.delete_flag
    }


def mantis_delete_test_milestone_tool(request_params):
    MantisTestMileStone.query.filter(
        MantisTestMileStone.id == request_params.get('id')
    ).delete()
    MantisTestCycle.query.filter(
        MantisTestCycle.linked_milestone == request_params.get('id')
    ).update({'linked_milestone': None})
    mantis_db.session.commit()


def get_test_milestone_by_id(test_milestone_id):
    mtm = MantisTestMileStone.query.filter(MantisTestMileStone.id == test_milestone_id).first()
    return mtm


def get_test_milestone_insight_graph_tool(params_dict):
    cycles = get_test_cycle_for_test_milestone(params_dict.get('linked_milestone'), params_dict.get('test_scenario'))
    insight = {}
    for cycle in cycles:
        if cycle.test_group not in insight.keys():
            insight[cycle.test_group] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for result_id, result_count in get_case_current_result(cycle.filter_config).items():
            insight[cycle.test_group] = dict(Counter(insight[cycle.test_group]) + Counter(result_count))
    return insight


def get_test_milestone_group_graph_tool(params_dict):
    cycles = get_test_cycle_for_test_milestone(
        params_dict.get('linked_milestone'),
        params_dict.get('test_scenario'),
        params_dict.get('group_id'),
    )
    insight = {}
    for cycle in cycles:
        if params_dict.get('test_scenario') == 1:
            for func_id, result_count in get_case_current_result(cycle.filter_config).items():
                if func_id not in insight.keys():
                    insight[func_id] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                insight[func_id] = dict(insight[func_id] + Counter(result_count))
        elif params_dict.get('test_scenario') == 2:
            for tester in cycle.free_test_item.keys():
                if cycle.free_test_item not in insight.keys():
                    insight[tester] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                for result_id, result_count in get_case_current_result(cycle.filter_config).items():
                    insight[tester] = dict(insight[tester] + Counter(result_count))
    return insight


def get_test_cycle_for_test_milestone(test_milestone_id, test_scenario, group_id=None):
    filter_list = [
        MantisTestCycle.linked_milestone == test_milestone_id, MantisTestCycle.test_scenario == test_scenario
    ]
    if group_id is not None:
        filter_list.append(MantisTestCycle.test_group == group_id)
    query_list = [MantisTestCycle.test_group, MantisTestCycle.free_test_item, MantisFilterRecord.filter_config]
    cycles = mantis_db.session.query(*query_list).json(
        MantisFilterRecord, MantisTestCycle.filter_id == MantisFilterRecord.id, isouter=True
    ).filter(*filter_list).all()
    return cycles


def get_case_current_result(filter_config, query_type=None):
    filter_list = parse_case_filter_config(filter_config)
    subquery = mantis_db.session.query(CaseResult.m_id, CaseResult.test_result).subquery()
    cr_alias = aliased(subquery, name='cr')
    common_query_list = [func.max(cr_alias.c.test_result), func.count(1).label('count')]
    if query_type == 'func':
        common_query_list = [func.max(TestCase.function)] + common_query_list
    result_number = mantis_db.session.query(*common_query_list).join(
        cr_alias, TestCase.id == cr_alias.c.m_id, isouter=True
    ).filter(*filter_list).group_by(cr_alias.c.test_result).all()
    ret = {}
    for row in result_number:
        result, count = row.test_result if row.test_result is not None else 4, row.count
        if query_type == 'func':
            func_id = row.function
            if func_id not in ret.keys():
                ret[func_id] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            ret[func_id][result] = count if result not in ret[func_id].keys() else ret[func_id][result] + count
        else:
            ret[result] = count if result not in ret.keys() else ret[result] + count
    return ret


def parse_case_filter_config(filter_config):
    filter_list = []
    case_column_dict = TestCase.get_field_dict()
    for key, values in filter_config.items():
        if key == 'fuLi_value':
            key = 'fuLi_id'
        if key not in case_column_dict.keys():
            continue
        if key.startswith('available_'):
            current_filter_list = []
            for value in values:
                func.json_contains(case_column_dict.get(key), str(value))
            if filter_config.get(f'{key}_logic') == 'or':
                filter_list.append(or_(*current_filter_list))
            elif filter_config.get(f'{key}_logic') == 'and':
                filter_list.append(and_(*current_filter_list))
        else:
            conditional_filter(filter_list, case_column_dict.get(key), values)
    return filter_list
