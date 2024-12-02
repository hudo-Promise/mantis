import json

from common_tools.tools import create_current_format_time, update_tool, get_gap_days, calculate_time_to_finish, \
    op11_redis_client
from mantis.controller.mantis_test_milestone_tool import get_test_milestone_by_id
from mantis.models import mantis_db
from mantis.models.mantis_test_milestone_cycle import MantisTestCycle


def mantis_create_test_cycle_tool(request_params):
    current_time = create_current_format_time()
    cluster = request_params.get('cluster')
    case_list = request_params.get('case_list', [])
    mantis_update_test_cycle_info(case_list, cluster)
    milestone = get_test_milestone_by_id(request_params.get('linked_milestone'))
    mtc = MantisTestCycle(
        linked_milestone=request_params.get('linked_milestone'),
        project=milestone.project,
        cluster=milestone.cluster,
        name=request_params.get('name'),
        description=request_params.get('description'),
        assignee=request_params.get('assignee'),
        status=1,
        start_date=request_params.get('start_date'),
        due_date=request_params.get('due_date'),
        create_time=current_time,
        update_time=current_time,
        delete_flag=0
    )
    mantis_db.session.add(mtc)
    mantis_db.session.commit()


def mantis_edit_test_cycle_tool(request_params):
    mtc = MantisTestCycle.query.filter(MantisTestCycle.id == request_params.get('id')).first()
    update_dict = {'update_time': create_current_format_time()}
    update_key = ['linked_milestone', 'name', 'description', 'status', 'due_date', 'delete_flag']
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
        'linked_milestone': mtc.linked_milestone,
        'project': mtc.project,
        'cluster': mtc.cluster,
        'name': mtc.name,
        'description': mtc.description,
        'assignee': mtc.assignee,
        'status': mtc.status,
        'start_date': mtc.start_date,
        'due_date': mtc.due_date,
        'time_left': get_gap_days(current_time, f'{mtc.due_date} 00:00:00') + 1,
        'actual_finish_date': mtc.actual_finish_date,
        'time_to_finish': calculate_time_to_finish(
            get_gap_days(f'{mtc.start_date} 00:00:00', current_time) + 1,
            0.9
        ),  # TODO
        'create_time': str(mtc.create_time),
        'update_time': str(mtc.update_time),
        'delete_flag': mtc.delete_flag
    }


def mantis_update_test_cycle_info(case_list, cluster):
    current_cases = {}
    for case in op11_redis_client.lrange(f'test_case_cache_{cluster}', 0, -1):
        case = json.loads(case)
        current_cases[case.get('m_id')] = case
    field_mapping = json.loads(op11_redis_client.get('field_id2value'))
    cycle_result = {"pass": 0, "tb": 0, "null": 0, "fail": 0, "tb_fnr": 0}
    for m_id in case_list:
        case = current_cases.get(m_id)
        case_result = case.get('case_result')
        if not case_result:
            continue


def mantis_delete_test_cycle_tool(request_params):
    MantisTestCycle.query.filter(
        MantisTestCycle.id == request_params.get('id')
    ).delete()
    mantis_db.session.commit()
