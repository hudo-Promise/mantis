# -*- coding: utf-8 -*-
from mantis.models import mantis_db


class Functions(mantis_db.Model):
    __tablename__ = 'functions'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    test_group = mantis_db.Column(mantis_db.Integer, nullable=False, comment='测试组')
    function = mantis_db.Column(mantis_db.String(64), nullable=False, comment='功能')


class SubFunction(mantis_db.Model):
    __tablename__ = 'sub_functions'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    test_group = mantis_db.Column(mantis_db.Integer, nullable=False, comment='测试组')
    function = mantis_db.Column(mantis_db.Integer, nullable=False, comment='功能')
    sub_function = mantis_db.Column(mantis_db.String(64), nullable=False, comment='子功能')


class Group(mantis_db.Model):
    __tablename__ = 'group'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    group_name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='测试组')


class MantisFuLiGroup(mantis_db.Model):
    __tablename__ = 'mantis_fuLi_group'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    fuLi_group_name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='fuLi组')


class MantisFuLi(mantis_db.Model):
    __tablename__ = 'mantis_fuLi'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    fuLi_id = mantis_db.Column(mantis_db.String(16), nullable=True, comment='fuLi ID')
    fuLi_desc = mantis_db.Column(mantis_db.String(512), nullable=True, comment='fuLi 描述')
    fuLi_group_id = mantis_db.Column(mantis_db.Integer, nullable=True, comment='fuLi组id')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=True, comment='删除标志 1 正常 2 删除')


class MantisCaseField(mantis_db.Model):
    __tablename__ = 'mantis_case_field'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, autoincrement=True, comment='主键')
    case_field = mantis_db.Column(mantis_db.String(32), nullable=True, comment='字段名')
    case_field_mapping = mantis_db.Column(mantis_db.JSON, nullable=True, comment='值名')
    comment = mantis_db.Column(mantis_db.String(512), nullable=True, comment='描述')
