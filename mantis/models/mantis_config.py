from mantis.models import mantis_db


class MantisMappingRule(mantis_db.Model):
    __tablename__ = 'mantis_mapping_rule'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    cluster_id = mantis_db.Column(mantis_db.Integer, nullable=True, comment='cluster 配置')
    mapping_name = mantis_db.Column(mantis_db.String(32), nullable=True, comment='mapping 名称')
    mapping_rule = mantis_db.Column(mantis_db.JSON, nullable=True, comment='mapping 配置')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='创建时间')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=True, comment='更新时间')
