import time

from sqlalchemy.sql import func

from common_tools.tools import (
    create_current_format_time, update_tool, get_gap_days, calculate_time_to_finish, generate_week_str,
    get_dates_by_week
)
from mantis.controller.mantis_test_milestone_tool import get_test_milestone_by_id, parse_case_filter_config, \
    get_case_current_result, get_test_cycle_for_graph, deal_week_time, calculate_label
from mantis.models import mantis_db
from mantis.models.case import TestCase, CaseResult
from mantis.models.mantis_test_milestone_cycle import MantisTestCycle


def mantis_create_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    free_test_item = generate_free_test_item(
        request_params.get('test_scenario'),
        request_params.get('tester'),
        request_params.get('free_test_item')
    )
    mtc = MantisTestCycle(
        name=request_params.get('name'),
        test_group=request_params.get('test_group'),
        linked_milestone=request_params.get('linked_milestone'),
        project=milestone.project,
        cluster=milestone.cluster,
        market=request_params.get('market'),
        start_date=get_dates_by_week(request_params.get('start_date')),
        due_date=get_dates_by_week(request_params.get('due_date')),
        description=request_params.get('description'),
        filter_id=request_params.get('filter_id'),
        test_scenario=request_params.get('test_scenario'),
        free_test_item=free_test_item,
        status=1,
        line=request_params.get('line'),
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
        'test_scenario', 'free_test_item', 'status', 'line'
    ]
    free_test_item = generate_free_test_item(
        request_params.get('test_scenario'),
        request_params.get('tester'),
        request_params.get('free_test_item')
    )
    request_params['free_test_item'] = free_test_item
    for key in ['start_date', 'due_date']:
        request_params[key] = get_dates_by_week(request_params.get(key))
    update_tool(update_dict, request_params, update_key, mtc)
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    update_dict['cluster'] = milestone.cluster
    update_dict['project'] = milestone.project
    MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).update(update_dict)
    mantis_db.session.commit()


def generate_free_test_item(test_scenario, testers, free_test_item):
    if test_scenario == 1:
        current_item = []
        for tester in testers:
            current_item.append({'desc': None, 'tester': tester, 'status': 0})
        return current_item
    elif test_scenario == 2:
        return free_test_item
    else:
        return free_test_item


def mantis_get_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    filter_list = [MantisTestCycle.cluster == request_params.get('cluster')]
    if request_params.get('start_date') and request_params.get('due_date'):
        for key in ['start_date', 'due_date']:
            request_params[key] = get_dates_by_week(request_params.get(key))
        filter_list.append(MantisTestCycle.start_date >= request_params.get('start_date'))
        filter_list.append(MantisTestCycle.due_date <= request_params.get('due_date'))
    if request_params.get('tester'):
        filter_list.append(
            func.JSON_EXTRACT(MantisTestCycle.free_test_item, '$[0].tester') == request_params.get('tester')
        )
    if request_params.get('status'):
        filter_list.append(getattr(MantisTestCycle, request_params.get('status')) == request_params.get('status'))
    mtc_list = MantisTestCycle.query.filter(*filter_list).all()
    ret = {}
    if not request_params.get('group_by'):
        ret[0] = list(map(lambda _mtc: generate_test_cycle_tool(current_time, _mtc), mtc_list))
    else:
        for mtc in mtc_list:
            cur_mtc = generate_test_cycle_tool(current_time, mtc)
            if getattr(cur_mtc, request_params.get('key')) not in ret.keys():
                ret[getattr(cur_mtc, request_params.get('key'))] = []
            ret[getattr(cur_mtc, request_params.get('key'))].append(cur_mtc)
    return ret


def mantis_get_test_cycle_by_milestone_tool(request_params):
    current_time = create_current_format_time()
    filter_list = [MantisTestCycle.linked_milestone == request_params.get('linked_milestone')]
    mtc_list = MantisTestCycle.query.filter(*filter_list).order_by(MantisTestCycle.test_group).all()
    group_line = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    cycle_group = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for mtc in mtc_list:
        cur_mtc = generate_test_cycle_tool(current_time, mtc)
        cycle_group[mtc.test_group].append(cur_mtc)
        if mtc.line > group_line.get(mtc.test_group, 0):
            group_line[mtc.test_group] = mtc.line
    ret = {
        'cycle_group': cycle_group,
        'group_line': group_line,
    }
    return ret


def generate_test_cycle_tool(current_time, mtc):
    start_year, due_year, start_week, due_week = deal_week_time(mtc)
    tester = [free_item.get('tester') for free_item in mtc.free_test_item]
    ret = {
        'id': mtc.id,
        'name': mtc.name,
        'test_group': mtc.test_group,
        'linked_milestone': mtc.linked_milestone,
        'project': mtc.project,
        'cluster': mtc.cluster,
        'market': mtc.market,
        'start_date': mtc.start_date,
        'start_week': f'{start_year}-{generate_week_str(mtc.start_date)}',
        'due_date': mtc.due_date,
        'due_week': f'{due_year}-{generate_week_str(mtc.due_date)}',
        'actual_finish_date': mtc.actual_finish_date,
        'description': mtc.description,
        'filter_id': mtc.filter_id,
        'test_scenario': mtc.test_scenario,
        'tester': tester,
        'free_test_item': mtc.free_test_item,
        'status': mtc.status,
        'time_left': get_gap_days(current_time, f'{mtc.due_date} 00:00:00') + 1,
        'time_to_finish': calculate_time_to_finish(
            get_gap_days(f'{mtc.start_date} 00:00:00', current_time) + 1,
            0.9
        ),  # TODO
        'line': mtc.line,
        'create_time': str(mtc.create_time),
        'update_time': str(mtc.update_time),
    }
    ret['label'] = calculate_label(ret.get('time_left'), ret.get('time_to_finish'))
    return ret


def mantis_delete_test_cycle_tool(request_params):
    MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).delete()
    mantis_db.session.commit()


def mantis_get_test_cycle_insight_graph_tool(params_dict):
    mtc = get_test_cycle_for_graph(
        {'id': params_dict.get('id')}
    )
    ret = get_case_current_result(mtc.filter_config, mtc.id, query_type=params_dict.get('query_type'))
    return ret


def mantis_get_test_cycle_burnout_diagram_tool(params_dict):
    mtc = get_test_cycle_for_graph({'id': params_dict.get('id')})
    if not mtc:
        return
    if not mtc.filter_config:
        return
    filter_list = parse_case_filter_config(mtc.filter_config)
    case_count = TestCase.query.filter(*filter_list).count()
    expect_data = {mtc.start_date: case_count, mtc.due_date: 0}
    burnout_data = mantis_db.session.query(
        func.date(CaseResult.upgrade_time).label('upgrade_date'),
        func.count(1).label('count')
    ).filter(
        CaseResult.cycle_id == mtc.id
    ).group_by(
        func.date(CaseResult.upgrade_time)
    ).order_by(func.date(CaseResult.upgrade_time)).all()
    burnout_dict = {}
    for burnout in burnout_data:
        burnout_dict[str(burnout.upgrade_date)] = case_count - burnout.count
        case_count -= burnout.count
    ret = {'expect_data': expect_data, 'burnout_data': burnout_dict}
    return ret


def mantis_get_test_cycle_pie_chart_tool(params_dict):
    mtc = get_test_cycle_for_graph({'id': params_dict.get('id')})
    ret = get_case_current_result(mtc.filter_config, mtc.id)
    return ret


def mantis_test_cycle_work_report_tool():
    year = time.localtime().tm_year
    start_time, end_time = f'{year}-01-01 00:00:00', f'{year}-12-31 23:59:59'
    rows = mantis_db.session.query(
        CaseResult.tester,
        func.date_format(CaseResult.upgrade_time, '%Y-%m').label('upgrade_time'),
        func.count(0).label('count')
    ).filter(
        CaseResult.upgrade_time >= start_time,
        CaseResult.upgrade_time <= end_time,
        CaseResult.cycle_id != 0
    ).group_by(CaseResult.tester, func.date_format(CaseResult.upgrade_time, '%Y-%m')).all()
    ret = {}
    for row in rows:
        if row.tester not in ret.keys():
            ret[row.tester] = {}
        if row.upgrade_time not in ret[row.tester].keys():
            ret[row.tester][row.upgrade_time] = row.count
    return ret
