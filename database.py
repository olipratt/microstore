import logging
import tinydb


log = logging.getLogger(__name__)

# Global variable to hold the database instance.
db = None


def init(backing_file=None):
    """Open the global database instance.

    :param backing_file: Name of file to back the database - None for in-memory
    """
    global db
    assert db is None

    if backing_file is None:
        log.debug("Opening in-memory database instance")
        db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)
    else:
        log.debug("Opening file-backed database instance: %r", backing_file)
        db = tinydb.TinyDB(backing_file)


def term():
    """Close the global database instance."""
    log.debug("Closing database instance")
    global db
    assert db is not None

    db.close()
    db = None


def _access_table(table_name):
    """Access the apps data database table."""
    global db
    assert db is not None
    return db.table(table_name)


def store(namespace, key, value):
    table = _access_table(namespace)
    if table.contains(tinydb.where('key') == key):
        table.update({'value': value}, tinydb.where('key') == key)
    else:
        table.insert({'key': key, 'value': value})


def retrieve(namespace, key):
    table = _access_table(namespace)
    element = table.get(tinydb.where('key') == key)
    if element is None:
        return None
    else:
        return element['value']


def delete(namespace, key):
    table = _access_table(namespace)
    table.remove(tinydb.where('key') == key)


def keys(namespace):
    table = _access_table(namespace)
    keys = [x["key"] for x in table.all()]
    return keys
