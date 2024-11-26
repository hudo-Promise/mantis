from common_tools.tools import create_current_format_time, get_gap_days, update_tool, calculate_time_to_finish
from mantis.models import mantis_db
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
