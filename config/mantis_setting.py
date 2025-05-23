# -*- coding: utf-8 -*-

from config.basic_setting import SERVICE_MODE, LINK_URL, InstanceConfig

mantis_api_dict = {
    'product': '/mantis-api',
    'develop': '/mantis-dev',
    'testing': '/mantis-test',
}

MANTIS_API = mantis_api_dict.get(SERVICE_MODE)
MANTIS_SECRET_KEY = "xxx"
GLOBAL_KEY_D = '88815'


instance_config = InstanceConfig('mantis_db')
swagger_config = instance_config.swagger_config(MANTIS_API)

template_config = instance_config.template_config("MANTIS")


mantis_url_prefix_dict = {
    'product': f'{LINK_URL}/mantis/#/shareCharts?unique_id=%s&type=share',
    'develop': f'{LINK_URL}/mantis_dev/#/shareCharts?unique_id=%s&type=share',
    'testing': f'{LINK_URL}/mantis_test/#/shareCharts?unique_id=%s&type=share'
}


mantis_share_url_prefix = mantis_url_prefix_dict.get(SERVICE_MODE)
