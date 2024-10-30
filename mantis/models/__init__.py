from common_tools.initialize import InitDB


mantis_db, mantis_db_bcrypt = InitDB.generate_db()


def init_db(app):
    mantis_db.init_app(app)
    mantis_db_bcrypt.init_app(app)
