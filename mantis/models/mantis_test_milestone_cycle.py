from mantis.models import mantis_db


class MantisTestMileStone(mantis_db.Model):
    __tablename__ = 'mantis_test_milestone'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='test milestone name')
    description = mantis_db.Column(mantis_db.Text, nullable=True, comment='描述')
    project = mantis_db.Column(mantis_db.Integer, nullable=True, comment='项目')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=False, comment='集群')
    status = mantis_db.Column(mantis_db.Integer, nullable=False, comment='状态')
    start_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='开始日期')
    due_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='截至日期')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')


class MantisTestCycle(mantis_db.Model):
    __tablename__ = 'mantis_test_cycle'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='test cycle name')
    test_group = mantis_db.Column(mantis_db.Integer, nullable=True, comment='测试组')
    linked_milestone = mantis_db.Column(mantis_db.Integer, nullable=False, comment='所属 test milestone')
    project = mantis_db.Column(mantis_db.Integer, nullable=True, comment='项目')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=False, comment='集群')
    market = mantis_db.Column(mantis_db.JSON, nullable=True, comment='市场')
    start_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='开始日期')
    due_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='截至日期')
    actual_finish_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='实际完成日期')
    description = mantis_db.Column(mantis_db.Text, nullable=True, comment='描述')
    filter_id = mantis_db.Column(mantis_db.Integer, nullable=True, comment='filter config')
    test_scenario = mantis_db.Column(mantis_db.Integer, nullable=True, comment='类型 1 test case 2 free test')
    free_test_item = mantis_db.Column(mantis_db.JSON, nullable=True, comment='测试人员记录')
    status = mantis_db.Column(mantis_db.Integer, nullable=False, comment='状态')
    progress = mantis_db.Column(mantis_db.Integer, nullable=False, default=0, comment='进度')
    line = mantis_db.Column(mantis_db.Integer, nullable=False, default=0, comment='位置')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')
