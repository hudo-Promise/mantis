# -*- coding: utf-8 -*-


from mantis.models import mantis_db


class TestCase(mantis_db.Model):
    __tablename__ = "test_case"
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    creator = mantis_db.Column(mantis_db.Integer, nullable=True, comment='创建人')
    category = mantis_db.Column(mantis_db.Integer, nullable=True, comment='测试类别 Spec/Validation')
    function = mantis_db.Column(mantis_db.Integer, nullable=False, comment='功能')
    sub_function = mantis_db.Column(mantis_db.Integer, nullable=False, comment='子功能')
    fuLi_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='fuli')
    level = mantis_db.Column(mantis_db.Integer, nullable=True, comment='测试用例等级 -- 有测试结果不可为空 F4/F6/F8')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=False, comment='集群  43/44/45')
    available_platform = mantis_db.Column(mantis_db.JSON, nullable=True, comment='平台 -- 有测试结果不可为空 PPC/PPE/All')
    available_carline = mantis_db.Column(mantis_db.JSON, nullable=False, comment='车系')
    available_variant = mantis_db.Column(mantis_db.JSON, nullable=False, comment='车辆规格')
    available_market = mantis_db.Column(mantis_db.JSON, nullable=False, comment='市场 CN/TW/HK/MC/JP/KR')
    available_language = mantis_db.Column(mantis_db.JSON, nullable=False, comment='语言 TCN/SCN/TW/EN/JP/KR')
    available_environment = mantis_db.Column(mantis_db.JSON, nullable=True, comment='环境  car/all')
    title = mantis_db.Column(mantis_db.Text, nullable=False, comment='标题、描述')
    precondition = mantis_db.Column(mantis_db.Text, nullable=False, comment='前置条件')
    action = mantis_db.Column(mantis_db.Text, nullable=False, comment='测试步骤')
    expectation = mantis_db.Column(mantis_db.Text, nullable=False, comment='测试期望结果')
    reference_spec = mantis_db.Column(mantis_db.Text, nullable=True, comment='参考标准')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    upgrade_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')

    @classmethod
    def get_field_dict(cls):
        return {
            'id': cls.id,
            'creator': cls.creator,
            'category': cls.category,
            'function': cls.function,
            'sub_function': cls.sub_function,
            'fuLi_id': cls.fuLi_id,
            'level': cls.level,
            'cluster': cls.cluster,
            'available_platform': cls.available_platform,
            'available_carline': cls.available_carline,
            'available_variant': cls.available_variant,
            'available_market': cls.available_market,
            'available_language': cls.available_language,
            'available_environment': cls.available_environment,
            'title': cls.title,
            'precondition': cls.precondition,
            'action': cls.action,
            'expectation': cls.expectation,
            'reference_spec': cls.reference_spec,
            'delete_flag': cls.delete_flag,
            'create_time': cls.create_time,
            'upgrade_time': cls.upgrade_time
        }


class CaseResult(mantis_db.Model):
    __tablename__ = 'case_result'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    m_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='唯一标识符')
    tester = mantis_db.Column(mantis_db.Integer, nullable=True, comment='测试人员')
    test_sw = mantis_db.Column(mantis_db.String(32), nullable=True, comment='软件版本 -- 有测试结果不可为空')
    sw_num = mantis_db.Column(mantis_db.Integer, nullable=True, comment='软件版本 -- 有测试结果不可为空')
    test_result = mantis_db.Column(mantis_db.Integer, nullable=True, comment='结果 pass fail tb empty n/a null')
    test_platform = mantis_db.Column(mantis_db.Integer, nullable=True, comment='平台 -- PPC/PPE/All')
    test_carline = mantis_db.Column(mantis_db.Integer, nullable=True, comment='车系  -- 有测试结果不可为空')
    test_variant = mantis_db.Column(mantis_db.Integer, nullable=True, comment='车辆规格 -- 有测试结果不可为空')
    test_market = mantis_db.Column(mantis_db.Integer, nullable=True, comment='市场  -- 有测试结果不可为空')
    test_language = mantis_db.Column(mantis_db.Integer, nullable=True, comment='语言 TCN/SCN/TW/EN/JP/KR')
    test_environment = mantis_db.Column(mantis_db.Integer, nullable=True, comment='环境  car/all')
    tb_type = mantis_db.Column(mantis_db.Integer, nullable=True, comment='用例停滞原因')
    issue_descr = mantis_db.Column(mantis_db.String(512), nullable=True, comment='阻挡用例')
    comments = mantis_db.Column(mantis_db.Text, nullable=True, comment='备注')
    extra_1 = mantis_db.Column(mantis_db.String(16), nullable=True, comment='补充数据1')
    extra_2 = mantis_db.Column(mantis_db.String(16), nullable=True, comment='补充数据2')
    extra_3 = mantis_db.Column(mantis_db.String(16), nullable=True, comment='补充数据3')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='创建时间')
    upgrade_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')

    @classmethod
    def get_field_dict(cls):
        return {
            'id': cls.id,
            'm_id': cls.m_id,
            'tester': cls.tester,
            'test_sw': cls.test_sw,
            'sw_num': cls.sw_num,
            'test_result': cls.test_result,
            'test_platform': cls.test_platform,
            'test_carline': cls.test_carline,
            'test_variant': cls.test_variant,
            'test_market': cls.test_market,
            'test_language': cls.test_language,
            'test_environment': cls.test_environment,
            'tb_type': cls.tb_type,
            'issue_descr': cls.issue_descr,
            'comments': cls.comments,
            'extra_1': cls.extra_1,
            'extra_2': cls.extra_2,
            'extra_3': cls.extra_3,
            'create_time': cls.create_time,
            'upgrade_time': cls.upgrade_time
        }


class SWMap(mantis_db.Model):
    __tablename__ = 'sw_map'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    sw_alpha = mantis_db.Column(mantis_db.String(8), primary_key=True, comment='主键')
    sw_num = mantis_db.Column(mantis_db.Integer, nullable=True, comment='软件版本 -- 有测试结果不可为空')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')


class MantisFilterRecord(mantis_db.Model):
    __tablename__ = 'mantis_filter_record'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    filter_name = mantis_db.Column(mantis_db.String(32), nullable=True, comment='名称')
    filter_desc = mantis_db.Column(mantis_db.String(256), nullable=True, comment='描述')
    creator = mantis_db.Column(mantis_db.Integer, nullable=True, comment='创建人')
    mapping_rule_id = mantis_db.Column(mantis_db.Integer, nullable=True, comment='mapping rule')
    filter_config = mantis_db.Column(mantis_db.JSON, nullable=True, comment='筛选配置')
    visibility_level = mantis_db.Column(mantis_db.Integer, nullable=False, comment='能见度  0 private 1 public')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')
