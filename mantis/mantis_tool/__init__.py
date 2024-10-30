from mantis.models.boards import MileStoneGroup, CardGroup


def query_group(query_id, query_type):
    group_dict = {}
    model_dict = {
        'milestone': MileStoneGroup,
        'card': CardGroup,
    }
    condition_dict = {
        'milestone': MileStoneGroup.milestone_id,
        'card': CardGroup.card_id,
    }
    from mantis.mantis_app import mantis_app
    with mantis_app.app_context():
        if isinstance(query_id, int):
            group = model_dict.get(query_type).query.filter(condition_dict.get(query_type) == query_id).first()
            get_query_group_result(group_dict, group, query_type)
        else:
            group_list = model_dict.get(query_type).query.filter(condition_dict.get(query_type).in_(query_id)).all()
            for group in group_list:
                get_query_group_result(group_dict, group, query_type)
    return group_dict


def get_query_group_result(group_dict, group, query_type):
    if query_type == 'milestone':
        group_dict[group.milestone_id] = group.milestone_group_result
    elif query_type == 'card':
        group_dict[group.card_id] = group.card_group_result
