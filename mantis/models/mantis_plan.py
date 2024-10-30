from mantis.models import mantis_db


class MantisPlan(mantis_db.Model):
    __tablename__ = 'mantis_plan'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    unique_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='唯一标识')
    name = mantis_db.Column(mantis_db.String(128), nullable=True, comment='计划名称')
    description = mantis_db.Column(mantis_db.Text, nullable=True, comment='计划描述')
    creator = mantis_db.Column(mantis_db.String(64), nullable=True, comment='创建人')
    project = mantis_db.Column(mantis_db.JSON, nullable=True, comment='项目类型')
    function = mantis_db.Column(mantis_db.JSON, nullable=True, comment='功能')
    sub_function = mantis_db.Column(mantis_db.JSON, nullable=True, comment='子功能')
    market = mantis_db.Column(mantis_db.JSON, nullable=True, comment='市场')
    language = mantis_db.Column(mantis_db.JSON, nullable=True, comment='语言')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=True, comment='集群')
    level = mantis_db.Column(mantis_db.JSON, nullable=True, comment='等级')
    platform = mantis_db.Column(mantis_db.JSON, nullable=True, comment='项目平台')
    carline = mantis_db.Column(mantis_db.JSON, nullable=True, comment='车型')
    case_list = mantis_db.Column(mantis_db.JSON, nullable=True, comment='case id list')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=True, comment='0 未删除 1 删除')
