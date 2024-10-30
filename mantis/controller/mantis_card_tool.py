from common_tools.async_api_tool import update_mantis_single_graph
from common_tools.tools import generate_uuid
from mantis.mantis_tool import query_group
from mantis.models import mantis_db
from mantis.models.boards import Card, CardGroup, BoardLocation


def create_card_func(request_params):
    """
    card_group_example
        {
            'xxx1': {
                'name': 'xxx',
                'sub_function': [1, 2, 3],
                'comment': 'xxx'
            }
        }
    """
    uuid = generate_uuid()
    card = Card(
        board_id=request_params.get('board_id'),
        name=request_params.get('name'),
        bar_type=request_params.get('bar_type'),
        cluster=request_params.get('cluster'),
        category=request_params.get('category'),
        available_carline=request_params.get('available_carline'),
        test_carline=request_params.get('test_carline'),
        available_market=request_params.get('available_market'),
        test_market=request_params.get('test_market'),
        available_language=request_params.get('available_language'),
        test_language=request_params.get('test_language'),
        available_variant=request_params.get('available_variant'),
        test_variant=request_params.get('test_variant'),
        available_environment=request_params.get('available_environment'),
        test_environment=request_params.get('test_environment'),
        available_platform=request_params.get('available_platform'),
        test_platform=request_params.get('test_platform'),
        level=request_params.get('level'),
        card_groups=deal_card_group_fuli(request_params.get('card_groups')),
        available_logic={
            'available_carline': request_params.get('available_carline_logic', 'or'),
            'available_variant': request_params.get('available_variant_logic', 'or'),
            'available_market': request_params.get('available_market_logic', 'or'),
            'available_language': request_params.get('available_language_logic', 'or'),
            'available_environment': request_params.get('available_environment_logic', 'or'),
            'available_platform': request_params.get('available_platform_logic', 'or'),
        }
    )
    mantis_db.session.add(card)
    mantis_db.session.flush()
    mantis_db.session.commit()
    update_mantis_single_graph(uuid, card.id, 'card')
    return uuid, card.id


def parse_edit_card_params(request_params):
    board_id = request_params.get('board_id')
    card_id = request_params.get('card_id')

    update_dict = {
        'name': request_params.get('name'),
        'cluster': request_params.get('cluster'),
        'category': request_params.get('category'),
        'available_carline': request_params.get('available_carline'),
        'test_carline': request_params.get('test_carline'),
        'available_variant': request_params.get('available_variant'),
        'test_variant': request_params.get('test_variant'),
        'available_market': request_params.get('available_market'),
        'test_market': request_params.get('test_market'),
        'available_language': request_params.get('available_language'),
        'test_language': request_params.get('test_language'),
        'available_environment': request_params.get('available_environment'),
        'test_environment': request_params.get('test_environment'),
        'available_platform': request_params.get('available_platform'),
        'test_platform': request_params.get('test_platform'),
        'level': request_params.get('level'),
        'card_groups': deal_card_group_fuli(request_params.get('card_groups')),
        'available_logic': {
            'available_carline': request_params.get('available_carline_logic', 'or'),
            'available_variant': request_params.get('available_variant_logic', 'or'),
            'available_market': request_params.get('available_market_logic', 'or'),
            'available_language': request_params.get('available_language_logic', 'or'),
            'available_environment': request_params.get('available_environment_logic', 'or'),
            'available_platform': request_params.get('available_platform_logic', 'or'),
        }
    }
    return board_id, card_id, update_dict


def deal_card_group_fuli(card_groups):
    current_group = {}
    for key, value in card_groups.items():
        current_group[key] = value
    return current_group


def edit_card_func(board_id, card_id, update_dict):
    Card.query.filter(
        Card.board_id == board_id, Card.id == card_id
    ).update(update_dict)
    mantis_db.session.commit()
    uuid = generate_uuid()
    update_mantis_single_graph(uuid, card_id, 'card')
    return uuid


def delete_card_func(card_id):
    Card.query.filter(Card.id.in_(card_id)).delete()
    CardGroup.query.filter(CardGroup.card_id.in_(card_id)).delete()
    mantis_db.session.commit()


def query_card_func(request_params):
    board_id = request_params.get('board_id')
    card_id = request_params.get('card_id')
    if card_id:
        card = Card.query.filter(Card.id == card_id).first()
        cg = query_group(int(card_id), 'card')
        bl = BoardLocation.query.filter(BoardLocation.board_id == board_id,
                                        BoardLocation.type == 'card',
                                        BoardLocation.data_id == card_id).first()
        result = {
            'board_id': bl.board_id,
            'location_id': bl.location_id,
            'type': bl.type,
            'length': bl.length,
            'width': bl.width,
            'data_id': bl.data_id,
            'data': generate_card(card, cg),
        }
        return result
    else:
        cards = Card.query.filter(Card.board_id == board_id).all()
        card_id = [item.id for item in cards]
        msg = query_group(card_id, 'card')
        return {card.id: generate_card(card, msg) for card in cards}


def generate_card(card, cg):
    card_dict = {
        'card_id': card.id,
        'board_id': card.board_id,
        'card_name': card.name,
        'bar_type': card.bar_type,
        'cluster': card.cluster,
        'category': card.category,
        'available_carline': card.available_carline,
        'test_carline': card.test_carline,
        'available_market': card.available_market,
        'test_market': card.test_market,
        'available_language': card.available_language,
        'test_language': card.test_language,
        'available_variant': card.available_variant,
        'test_variant': card.test_variant,
        'available_environment': card.available_environment,
        'test_environment': card.test_environment,
        'available_platform': card.available_platform,
        'test_platform': card.test_platform,
        'level': card.level,
        'card_groups': cg.get(card.id),
        'available_logic': card.available_logic
    }
    return card_dict
