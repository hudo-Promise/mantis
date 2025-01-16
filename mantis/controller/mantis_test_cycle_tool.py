import json
import time

from sqlalchemy import Integer
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from common_tools.tools import (
    create_current_format_time, update_tool, get_gap_days, calculate_time_to_finish, generate_week_str,
    get_dates_by_week, generate_dates, op11_redis_client
)
from config.basic_setting import FORMAT_DATE
from mantis.controller.mantis_test_milestone_tool import get_test_milestone_by_id, parse_case_filter_config, \
    get_case_current_result, get_test_cycle_for_graph, deal_week_time, calculate_label, generate_axis_data
from mantis.mantis_status import mtc_groups
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
    test_scenario = request_params.get('test_scenario')
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
        test_scenario=test_scenario,
        free_test_item=free_test_item,
        status=1,
        line=request_params.get('line'),
        create_time=current_time,
        update_time=current_time,
    )
    mantis_db.session.add(mtc)
    mantis_db.session.flush()
    cycle_id = mtc.id
    mantis_db.session.commit()


def mantis_edit_test_cycle_tool(request_params):
    cycle_id = request_params.get('id')
    test_scenario = request_params.get('test_scenario')
    mtc = MantisTestCycle.query.filter(MantisTestCycle.id == cycle_id).first()
    update_dict = {'update_time': create_current_format_time()}
    update_key = [
        'name', 'test_group', 'linked_milestone', 'market', 'start_date', 'due_date', 'description', 'filter_id',
        'test_scenario', 'free_test_item', 'status', 'line'
    ]
    free_test_item = generate_free_test_item(
        test_scenario,
        request_params.get('tester'),
        request_params.get('free_test_item')
    )
    for key in ['start_date', 'due_date']:
        if not request_params.get(key):
            continue
        if len(request_params.get(key).split('-')) == 2:
            request_params[key] = get_dates_by_week(request_params.get(key))
    request_params['free_test_item'] = free_test_item
    update_tool(update_dict, request_params, update_key, mtc)
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    update_dict['cluster'] = milestone.cluster
    update_dict['project'] = milestone.project
    MantisTestCycle.query.filter(MantisTestCycle.id == cycle_id).update(update_dict)
    mantis_db.session.commit()


def generate_free_test_item(test_scenario, testers, free_test_item):
    if test_scenario == 1:
        current_item = []
        for tester in testers:
            current_item.append({'desc': None, 'tester': tester, 'status': 1})
        return current_item
    elif test_scenario == 2:
        return free_test_item
    else:
        return free_test_item


def mantis_get_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    filter_list = [MantisTestCycle.cluster == request_params.get('cluster')]
    if request_params.get('start_date') and request_params.get('due_date'):
        filter_list.append(MantisTestCycle.start_date >= request_params.get('start_date'))
        filter_list.append(MantisTestCycle.due_date <= request_params.get('due_date'))
    if request_params.get('tester'):
        filter_list.append(
            func.JSON_EXTRACT(
                MantisTestCycle.free_test_item, '$[0].tester'
            ).cast(Integer).in_(request_params.get('tester'))
        )
    if request_params.get('test_group'):
        filter_list.append(MantisTestCycle.test_group == request_params.get('test_group'))
    filter_list.append(getattr(MantisTestCycle, 'status') == request_params.get('status', 1))
    mtc_list = MantisTestCycle.query.filter(*filter_list).all()
    ret = {}
    group_by_key = request_params.get('group_by', 'linked_milestone')
    for mtc in mtc_list:
        cur_mtc = generate_test_cycle_tool(current_time, mtc)
        if cur_mtc.get(group_by_key) not in ret.keys():
            ret[cur_mtc.get(group_by_key)] = []
        ret[cur_mtc.get(group_by_key)].append(cur_mtc)
    return ret


def mantis_get_test_cycle_by_milestone_tool(request_params):
    current_time = create_current_format_time()
    filter_list = [MantisTestCycle.linked_milestone == request_params.get('linked_milestone')]
    mtc_list = MantisTestCycle.query.filter(*filter_list).order_by(MantisTestCycle.test_group).all()
    group_line, cycle_group = {}, {}
    for group_id in mtc_groups:
        group_line[group_id] = 0
        cycle_group[group_id] = []
    for mtc in mtc_list:
        if mtc.test_group not in cycle_group.keys():
            cycle_group[mtc.test_group] = []
        if mtc.test_group not in group_line.keys():
            group_line[mtc.test_group] = 0
        if mtc.line > group_line.get(mtc.test_group, 0):
            group_line[mtc.test_group] = mtc.line
        cur_mtc = generate_test_cycle_tool(current_time, mtc)
        cycle_group[mtc.test_group].append(cur_mtc)
    ret = {'cycle_group': cycle_group, 'group_line': group_line}
    return ret


def generate_test_cycle_tool(current_time, mtc):
    start_year, due_year, start_week, due_week = deal_week_time(mtc)
    tester = [free_item.get('tester') for free_item in mtc.free_test_item]
    if mtc.test_scenario == 1:
        progress = calculate_test_cycle_pregress_for_test_case(mtc.id)
    else:
        progress = calculate_test_cycle_pregress_for_free_item(mtc.free_test_item)
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
            progress
        ) if progress != 0 else 0,  # TODO
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
    mtc = get_test_cycle_for_graph({'id': params_dict.get('id')})
    if mtc.test_scenario == 1:
        ret = mantis_get_test_cycle_insight_graph_test_case_tool(mtc, params_dict)
    elif mtc.test_scenario == 2:
        ret = mantis_get_test_cycle_insight_graph_free_test_tool(params_dict)
    else:
        ret = {}
    return ret


def mantis_get_test_cycle_insight_graph_test_case_tool(mtc, params_dict):
    result = get_case_current_result(
        mtc.filter_config,
        mtc.id,
        query_type=params_dict.get('query_type')
    )
    if params_dict.get('query_type') == 'function':
        ret = generate_axis_data(result, 1)
    elif params_dict.get('query_type') == 'tester':
        ret = generate_axis_data(result, 2)
    else:
        ret = {}
    return ret


def mantis_get_test_cycle_insight_graph_free_test_tool(params_dict):
    mtc = MantisTestCycle.query.filter(MantisTestCycle.id == params_dict.get('id')).first()
    ret = {}
    for free_test_item in mtc.free_test_item:
        if free_test_item.get('tester') not in ret.keys():
            ret[free_test_item.get('tester')] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ret[free_test_item.get('tester')][free_test_item.get('status')] += 1
    generate_axis_data(ret, 1)
    return generate_axis_data(ret, 1)


def mantis_get_test_cycle_burnout_diagram_tool(params_dict):
    mtc = get_test_cycle_for_graph({'id': params_dict.get('id')})
    if not mtc:
        return
    if not mtc.filter_config:
        return
    filter_list = parse_case_filter_config(mtc.filter_config)
    case_count = TestCase.query.filter(*filter_list).count()
    expect_date = [i.strftime(FORMAT_DATE) for i in generate_dates(str(mtc.start_date), str(mtc.due_date))]
    burnout_data = mantis_db.session.query(
        func.date(CaseResult.upgrade_time).label('upgrade_date'),
        func.count(1).label('count')
    ).filter(
        CaseResult.cycle_id == mtc.id
    ).group_by(
        func.date(CaseResult.upgrade_time)
    ).order_by(func.date(CaseResult.upgrade_time)).all()
    daily_finish_num = {}
    for burnout in burnout_data:
        daily_finish_num[str(burnout.upgrade_date)] = burnout.count
    burnout = []
    for i in range(0, len(expect_date)):
        if i == 0:
            if daily_finish_num.get(expect_date[i]):
                current_count = case_count - daily_finish_num.get(expect_date[i])
            else:
                current_count = case_count
        else:
            if daily_finish_num.get(expect_date[i]):
                current_count = burnout[i-1] - daily_finish_num.get(expect_date[i])
            else:
                current_count = burnout[i-1]
        burnout.append(current_count)
    ret = {'expect_data': expect_date, 'start_num': case_count, 'burnout_data': burnout}
    return ret


def mantis_get_test_cycle_pie_chart_tool(params_dict):
    mtc = MantisTestCycle.query.filter(MantisTestCycle.id == params_dict.get('id')).first()
    ret = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for free_test_item in mtc.free_test_item:
        ret[free_test_item.get('status')] += 1
    status_num = {}
    for key, value in ret.items():
        status_num[key] = value
    return status_num


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
            ret[row.tester] = {i: 0 for i in range(1, 13)}
        ret[row.tester][int(row.upgrade_time[6:])] = row.count
    axis = sorted(ret.keys())
    month_data = {i: [] for i in range(1, 13)}
    for user in axis:
        for i in range(1, 13):
            month_data[i].append(ret[user][i])
    return {'axis': axis, 'month_data': month_data}


def mantis_get_test_cycle_group_info_tool():
    op11_group_info = json.loads(op11_redis_client.get('tms_dept_and_group_info')).get('groups')
    result = {}
    for group_id in mtc_groups:
        result[group_id] = op11_group_info.get(str(group_id)).get('group')
    return result


def mantis_get_test_case_by_test_cycle_tool(param_dict):
    cycle_id = param_dict.get('cycle_id')
    page_num = int(param_dict.get('page_num'))
    page_size = int(param_dict.get('page_size'))
    query_type = int(param_dict.get('query_type'))
    cycle = get_test_cycle_for_graph({'id': cycle_id})
    filter_list = parse_case_filter_config(cycle.filter_config)
    if not filter_list:
        return None
    subquery = mantis_db.session.query(
        CaseResult.m_id,
        CaseResult.test_sw,
        CaseResult.test_result,
        CaseResult.test_platform,
        CaseResult.test_carline,
        CaseResult.test_variant,
        CaseResult.test_market,
        CaseResult.test_language,
        CaseResult.test_environment,
        CaseResult.tb_type,
        CaseResult.issue_descr,
        CaseResult.tester
    ).filter(
        CaseResult.cycle_id == cycle_id
    ).subquery()
    cr_alias = aliased(subquery, name='cr')
    if query_type == 1:
        filter_list.append(cr_alias.c.test_result.isnot(None))
    elif query_type == 2:
        filter_list.append(cr_alias.c.test_result.is_(None))
    cases = mantis_db.session.query(
        TestCase.id,
        TestCase.title,
        TestCase.function,
        TestCase.sub_function,
        cr_alias.c.test_sw,
        cr_alias.c.test_result,
        cr_alias.c.test_platform,
        cr_alias.c.test_carline,
        cr_alias.c.test_variant,
        cr_alias.c.test_market,
        cr_alias.c.test_language,
        cr_alias.c.test_environment,
        cr_alias.c.tb_type,
        cr_alias.c.issue_descr,
        cr_alias.c.tester
    ).select_from(TestCase).join(
        cr_alias, TestCase.id == cr_alias.c.m_id, isouter=True
    ).filter(*filter_list).offset((page_num - 1) * page_size).limit(page_size).all()
    total = mantis_db.session.query(
        TestCase.id,
    ).select_from(TestCase).join(
        cr_alias, TestCase.id == cr_alias.c.m_id, isouter=True
    ).filter(*filter_list).count()
    ret = []
    for case in cases:
        case = generate_case_for_cycle(case)
        ret.append(case)
    return {'case': ret, 'total': total}


def generate_case_for_cycle(case):
    return {
        'id': case.id,
        'title': case.title,
        'function': case.function,
        'sub_function': case.sub_function,
        'test_sw': case.test_sw,
        'test_result': case.test_result,
        'test_platform': case.test_platform,
        'test_carline': case.test_carline,
        'test_variant': case.test_variant,
        'test_market': case.test_market,
        'test_language': case.test_language,
        'test_environment': case.test_environment,
        'tb_type': case.tb_type,
        'issue_descr': case.issue_descr,
        'tester': case.tester
    }


def calculate_test_cycle_pregress_for_test_case(cycle_id):
    """
    更新case、result / 创建 编辑 test cycle / filter 变更
    """
    cycle = get_test_cycle_for_graph({'id': cycle_id})
    filter_list = parse_case_filter_config(cycle.filter_config)
    if not filter_list:
        return None
    finish_num = mantis_db.session.query(CaseResult.m_id).filter(
        CaseResult.cycle_id == cycle_id
    ).count()
    total = mantis_db.session.query(TestCase.id).filter(*filter_list).count()
    return round(finish_num / total, 2)


def calculate_test_cycle_pregress_for_free_item(free_items):
    finish_num = 0
    for item in free_items:
        if item.get('status') > 2:
            finish_num += 1
    return round(finish_num / len(free_items), 2)
