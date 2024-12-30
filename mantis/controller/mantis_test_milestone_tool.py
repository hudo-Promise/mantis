import time
from collections import Counter

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import aliased

from common_tools.tools import create_current_format_time, get_gap_days, update_tool, calculate_time_to_finish, \
    conditional_filter, generate_week, get_first_and_last_day, generate_week_str, get_weeks_around_year, \
    get_dates_by_week
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
        start_date=get_dates_by_week(request_params.get('start_date')),
        due_date=get_dates_by_week(request_params.get('due_date')),
        create_time=current_time,
        update_time=current_time,
    )
    mantis_db.session.add(mtm)
    mantis_db.session.commit()


def mantis_edit_test_milestone_tool(request_params):
    mtm = MantisTestMileStone.query.filter(MantisTestMileStone.id == request_params.get('id')).first()
    update_dict = {'update_time': create_current_format_time()}
    update_key = ['name', 'description', 'project', 'cluster', 'status', 'start_date', 'due_date']
    for key in ['start_date', 'due_date']:
        request_params[key] = get_dates_by_week(request_params.get(key))
    update_tool(update_dict, request_params, update_key, mtm)
    MantisTestMileStone.query.filter(MantisTestMileStone.id == request_params.get('id')).update(update_dict)
    mantis_db.session.commit()


def mantis_get_test_milestone_tool(request_params):
    current_time = create_current_format_time()
    mtms = MantisTestMileStone.query.filter(MantisTestMileStone.cluster == request_params.get('cluster')).all()
    return list(map(lambda mtm: generate_test_milestone_tool(current_time, mtm), mtms))


def mantis_get_test_milestone_time_table_tool():
    year, month, day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
    week = generate_week(f'{year}-{month}-{day}')
    left_day, _ = get_first_and_last_day(year if month != 1 else year - 1, month - 1 if month != 1 else 12)
    _, right_day = get_first_and_last_day(year if month != 12 else year + 1, month + 1 if month != 12 else 1)
    time_node = {
        'left_node': f'{year if month != 1 else year - 1}-{generate_week_str(left_day)}',
        'middle_node': f'{year}-{week if len(str(week)) == 2 else "0" + str(week)}',
        'right_node': f'{year if month != 12 else year + 1}-{generate_week_str(right_day)}'
    }
    ret = {
        'week': get_weeks_around_year(),
        'time_node': time_node,
    }
    return ret


def generate_test_milestone_tool(current_time, mtm):
    start_year, due_year, start_week, due_week = deal_week_time(mtm)
    mtm = {
        'id': mtm.id,
        'name': mtm.name,
        'description': mtm.description,
        'project': mtm.project,
        'cluster': mtm.cluster,
        'status': mtm.status,
        'start_date': mtm.start_date,
        'start_week': f'{start_year}-{generate_week_str(mtm.start_date)}',
        'due_date': mtm.due_date,
        'due_week': f'{due_year}-{generate_week_str(mtm.due_date)}',
        'time_left': get_gap_days(current_time, f'{mtm.due_date} 00:00:00') + 1,
        'time_to_finish': calculate_time_to_finish(
            get_gap_days(f'{mtm.start_date} 00:00:00', current_time) + 1,
            0.9
        ),  # TODO
        'create_time': str(mtm.create_time),
        'update_time': str(mtm.update_time),
    }
    return mtm


def deal_week_time(mtc):
    start_year, due_year = mtc.start_date[:4], mtc.due_date[:4]
    start_week, due_week = generate_week_str(mtc.start_date), generate_week_str(mtc.due_date)
    if mtc.start_date[5:7] == '12' and start_week == '01':
        start_year = str(int(start_year) + 1)
    if mtc.due_date[5:7] == '12' and due_week == '01':
        due_year = str(int(due_year) + 1)
    return start_year, due_year, start_week, due_week


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
    cycles = get_test_cycle_for_graph(
        {
            'linked_milestone': params_dict.get('linked_milestone'),
            'test_scenario': params_dict.get('test_scenario'),
        }
    )
    insight = {}
    for cycle in cycles:
        if cycle.test_group not in insight.keys():
            insight[cycle.test_group] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for result_id, result_count in get_case_current_result(cycle.filter_config, cycle.id).items():
            insight[cycle.test_group] = dict(Counter(insight.get(cycle.test_group)) + Counter(result_count))
    return insight


def get_test_milestone_group_graph_tool(params_dict):
    cycles = get_test_cycle_for_graph(
        {
            'linked_milestone': params_dict.get('linked_milestone'),
            'test_scenario': params_dict.get('test_scenario'),
            'group_id': params_dict.get('group_id'),
        }
    )
    insight = {}
    for cycle in cycles:
        if params_dict.get('test_scenario') == 1:
            for func_id, result_count in get_case_current_result(
                    cycle.filter_config, cycle.id, 'function').items():
                if func_id not in insight.keys():
                    insight[func_id] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                insight[func_id] = dict(Counter(insight.get(func_id)) + Counter(result_count))
        elif params_dict.get('test_scenario') == 2:
            for tester in cycle.free_test_item.keys():
                if cycle.free_test_item not in insight.keys():
                    insight[tester] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                for result_id, result_count in get_case_current_result(
                        cycle.filter_config, cycle.id, 'tester').items():
                    insight[tester] = dict(insight[tester] + Counter(result_count))
    return insight


def get_test_cycle_for_graph(params_dict):
    filter_list = [getattr(MantisTestCycle, key) == value for key, value in params_dict.items()]
    query_list = [
        MantisTestCycle.id,
        MantisTestCycle.test_group,
        MantisTestCycle.free_test_item,
        MantisFilterRecord.filter_config
    ]
    if 'id' in params_dict.keys():
        cycles = mantis_db.session.query(*query_list).json(
            MantisFilterRecord,
            MantisTestCycle.filter_id == MantisFilterRecord.id,
            isouter=True
        ).filter(*filter_list).first()
    else:
        cycles = mantis_db.session.query(*query_list).json(
            MantisFilterRecord,
            MantisTestCycle.filter_id == MantisFilterRecord.id,
            isouter=True
        ).filter(*filter_list).all()
    return cycles


def get_case_current_result(filter_config, cycle_id, query_type=None):
    filter_list = parse_case_filter_config(filter_config)
    subquery = mantis_db.session.query(CaseResult.m_id, CaseResult.test_result).filter(
        CaseResult.cycle_id == cycle_id
    ).subquery()
    cr_alias = aliased(subquery, name='cr')
    common_query_list = [func.max(cr_alias.c.test_result), func.count(1).label('count')]
    group_list = [cr_alias.c.test_result]
    if query_type == 'function':
        common_query_list = [func.max(getattr(TestCase, query_type))] + common_query_list
        group_list = [getattr(TestCase, query_type)] + group_list
    elif query_type == 'tester':
        common_query_list = [getattr(CaseResult, query_type)] + common_query_list
        group_list = [getattr(CaseResult, query_type)] + group_list
    result_number = mantis_db.session.query(*common_query_list).join(
        cr_alias, TestCase.id == cr_alias.c.m_id, isouter=True
    ).filter(*filter_list).group_by(*group_list).all()
    ret = {}
    for row in result_number:
        result, count = row.test_result if row.test_result is not None else 4, row.count
        if query_type:
            key = getattr(row, query_type)
            if key not in ret.keys():
                ret[key] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            ret[key][result] = count if result not in ret[key].keys() else ret[key][result] + count
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


def mantis_test_milestone_group_order_tool(params_dict):
    cycles = mantis_db.session.query(
        func.max(MantisTestCycle.test_group).label('test_group')
    ).filter_by(
        MantisTestCycle.linked_milestone == params_dict.get('linked_milestone')
    ).group_by(MantisTestCycle.linked_milestone).order_by(MantisTestCycle.linked_milestone).all()
    ret = [cycle.test_group for cycle in cycles]
    return ret
