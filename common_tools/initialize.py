# -*- coding: utf-8 -*-

import os

from flasgger import Swagger
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from common_tools.tools import global_logger
from config.basic_setting import DIR_PATH


class InitApp(object):
    def __init__(self, config, init_bp, init_db, service_mode, db, template_config, swagger_config,
                 activate_cache=None, init_scheduler=None):
        self.config = config
        self.init_bp = init_bp
        self.init_db = init_db
        self.service_mode = service_mode
        self.db = db
        self.template_config = template_config
        self.swagger_config = swagger_config
        self.activate_cache = activate_cache
        self.init_scheduler = init_scheduler

    def create_app(self):
        service_app = Flask(__name__)
        CORS(service_app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        Swagger(service_app, template=self.template_config, config=self.swagger_config)
        service_app.config.from_object(self.config)
        service_app.logger = global_logger
        self.init_bp(service_app)
        self.init_db(service_app)
        if self.activate_cache:
            self.activate_cache()
        if self.init_scheduler:
            self.init_scheduler(service_app)
        self.init()
        return service_app

    @classmethod
    def init(cls):
        if not os.path.exists(DIR_PATH):
            os.makedirs(DIR_PATH)


class InitDB(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_db():
        db = SQLAlchemy()
        db_bcrypt = Bcrypt()
        return db, db_bcrypt
