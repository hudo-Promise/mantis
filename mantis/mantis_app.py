# -*- coding: utf-8 -*-

from config.mantis_setting import *
from mantis.mantis_async_task.mantis_scheduled_task import init_scheduler
from mantis.mantis_caches import activate_cache
from mantis.models import init_db, mantis_db
from mantis.routes import init_bp
from common_tools.initialize import InitApp


init_app = InitApp(
    config=instance_config,
    init_bp=init_bp,
    init_db=init_db,
    service_mode=SERVICE_MODE,
    db=mantis_db,
    template_config=template_config,
    swagger_config=swagger_config,
    activate_cache=activate_cache,
    init_scheduler=init_scheduler
)


mantis_app = init_app.create_app()
