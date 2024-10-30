from common_tools.middleware import middleware_blueprint
from config.basic_setting import VERSION
from mantis.controller.mantis_board_view import board_blueprint
from mantis.controller.mantis_card_view import card_blueprint
from mantis.controller.mantis_case_view import case_blueprint
from mantis.controller.mantis_mapping_rule_view import mantis_mapping_rule_blueprint
from mantis.controller.mantis_common_view import mantis_common_blueprint
from mantis.controller.mantis_function_view import function_blueprint
from mantis.controller.mantis_milestone_view import milestone_blueprint
from mantis.controller.mantis_plan_view import mantis_plan_blueprint
from mantis.controller.mantis_share_record_view import share_record_blueprint
from mantis.controller.mantis_test_cycle_view import test_cycle_blueprint
from mantis.controller.mantis_test_milestone_view import test_milestone_blueprint
from mantis.mantis_tool.mantis_middleware import mantis_middleware_blueprint


def init_bp(app):
    app.register_blueprint(middleware_blueprint)
    app.register_blueprint(mantis_middleware_blueprint)

    app.register_blueprint(card_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(case_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(board_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(function_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(milestone_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(mantis_plan_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(share_record_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(mantis_common_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(mantis_mapping_rule_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(test_milestone_blueprint, url_prefix='/{version}/'.format(version=VERSION))
    app.register_blueprint(test_cycle_blueprint, url_prefix='/{version}/'.format(version=VERSION))
