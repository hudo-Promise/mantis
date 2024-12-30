from mantis.models import mantis_db
from mantis.models.mantis_project import MantisProject


def mantis_create_project_tool(params_dict):
    mp = MantisProject(project=params_dict.get('project'))
    mantis_db.session.add(mp)
    mantis_db.session.commit()


def mantis_edit_project_tool(params_dict):
    MantisProject.query.filter(
        MantisProject.project == params_dict.get('id')
    ).update({'project': params_dict.get('project')})
    mantis_db.session.commit()


def mantis_delete_project_tool(params_dict):
    MantisProject.query.filter(
        MantisProject.project == params_dict.get('id')
    ).delete()
    mantis_db.session.commit()


def mantis_get_project_tool(params_dict):
    mps = MantisProject.query.filter(
        MantisProject.project == params_dict.get('id')
    ).all()
    return [{'id': mp.id, 'project': mp.project} for mp in mps]
