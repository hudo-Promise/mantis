from mantis.models import mantis_db


class MantisProject(mantis_db.Model):
    __tablename__ = 'mantis_project'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    project = mantis_db.Column(mantis_db.String(32), nullable=True, comment='mapping 名称')
