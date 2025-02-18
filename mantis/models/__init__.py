from common_tools.initialize import InitDB
from datetime import datetime

mantis_db, mantis_db_bcrypt = InitDB.generate_db()


def init_db(app):
    mantis_db.init_app(app)
    mantis_db_bcrypt.init_app(app)


class DbBase(mantis_db.Model):
    __abstract__ = True

    def to_dict(self):
        return {
            c.name: getattr(self, c.name) if not type(getattr(self, c.name)) == datetime else str(getattr(self, c.name))
            for c in self.__table__.columns}