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
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')


class MantisTestCycle(mantis_db.Model):
    __tablename__ = 'mantis_test_cycle'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    linked_milestone = mantis_db.Column(mantis_db.Integer, nullable=False, comment='所属 test milestone')
    name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='test cycle name')
    description = mantis_db.Column(mantis_db.Text, nullable=True, comment='描述')
    assignee = mantis_db.Column(mantis_db.Integer, nullable=False, comment='关联人')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=False, comment='集群')
    status = mantis_db.Column(mantis_db.Integer, nullable=False, comment='状态')
    start_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='开始日期')
    due_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='截至日期')
    case_list = mantis_db.Column(mantis_db.JSON, nullable=True, comment='case id')
    cycle_result = mantis_db.Column(mantis_db.JSON, nullable=True, comment='统计结果')
    progress = mantis_db.Column(mantis_db.JSON, nullable=True, comment='完成进度')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')
