import atexit
import fcntl

from flask_apscheduler import APScheduler

from mantis.mantis_caches import activate_cache

scheduler = APScheduler()


def init_scheduler(app):
    f = open('./lock_file/mantis_scheduler.lock', 'wb')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(id="mantis_activate_cache", func=activate_cache,
                          trigger="cron", hour=5, minute=10, second=5)
    except Exception as e:
        print(e)

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)
