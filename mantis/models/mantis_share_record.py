from mantis.models import mantis_db


class MantisShareRecord(mantis_db.Model):
    __tablename__ = 'mantis_share_record'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    unique_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='唯一标识')
    sender = mantis_db.Column(mantis_db.Integer, nullable=False, comment='发送人')
    share_type = mantis_db.Column(mantis_db.Integer, nullable=False, comment='分享类型')
    receiver = mantis_db.Column(mantis_db.JSON, nullable=True, comment='接收人')
    status = mantis_db.Column(mantis_db.String(64), nullable=False, comment='状态 1 未读 2 已读')
    content = mantis_db.Column(mantis_db.JSON, nullable=False, comment='内容')
    config = mantis_db.Column(mantis_db.JSON, nullable=False, comment='配置')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')


class MantisOperateRecord(mantis_db.Model):
    __tablename__ = 'mantis_operate_record'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    operator = mantis_db.Column(mantis_db.Integer, nullable=True, comment='操作人')
    operator_name = mantis_db.Column(mantis_db.String(64), nullable=True, comment='操作人姓名')
    operate_url = mantis_db.Column(mantis_db.String(128), nullable=True, comment='访问路径')
    operate_content = mantis_db.Column(mantis_db.JSON, nullable=True, comment='操作内容')
    operate_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='操作时间')
