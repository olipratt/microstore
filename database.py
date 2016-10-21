import logging
import tinydb


log = logging.getLogger(__name__)
db = None
APPS_TABLE = "apps"


def init(backing_file=None):
    global db

    if backing_file is None:
        db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)
    else:
        db = tinydb.TinyDB(backing_file)


def term():
    global db
    db.close()
    db = None


def apps_list():
    global db

    table = db.table(APPS_TABLE)
    apps = [x["name"] for x in table.all()]
    return apps


def apps_find(app_name):
    global db

    table = db.table(APPS_TABLE)
    App = tinydb.Query()
    app = table.search(App.name == app_name)

    if len(app) == 0:
        return None
    else:
        assert len(app) == 1
        return app[0]


def apps_delete(app_name):
    global db

    table = db.table(APPS_TABLE)
    App = tinydb.Query()
    table.remove(App.name == app_name)


def apps_create(app_name, app_data):
    global db

    table = db.table(APPS_TABLE)
    table.insert({'name': app_name, 'data': app_data})


def apps_get(app_name):
    app = apps_find(app_name)

    if app is None:
        return None
    else:
        return app.get("data")


def apps_update(app_name, app_data):
    app = apps_find(app_name)
    if app is not None:
        apps_delete(app_name)

    apps_create(app_name, app_data)
