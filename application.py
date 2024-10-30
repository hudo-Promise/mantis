# -*- coding: utf-8 -*-

from config.mantis_setting import MANTIS_API
from mantis.mantis_app import mantis_app


app_dict = {
    MANTIS_API: mantis_app,
}

app = mantis_app
