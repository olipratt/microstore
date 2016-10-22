'''
A simple key-value store, which can be in-memory or JSON file backed.

>>> import kvstore

>>> kvstore.open()

>>> kvstore.store("mynamespace", "mykey", {"my": "value object"})

>>> kvstore.retrieve("mynamespace", "mykey")
{"my": "value object"}
>>> kvstore.keys("mynamespace")
["mykey"]
>>> kvstore.delete("mynamespace", "mykey")

>>> kvstore.keys("mynamespace")
[]
>>> kvstore.close()

'''
import logging
import tinydb


log = logging.getLogger(__name__)

# Global variable to hold the database instance.
db = None


def open(backing_file=None):
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


def close():
    """Close the global database instance."""
    log.debug("Closing database instance")
    global db
    assert db is not None

    db.close()
    db = None


def _retrieve_table(table_name):
    """Retrieve the database table with the supplied name."""
    global db
    assert db is not None
    return db.table(table_name)


def store(namespace, key, value):
    """Store a value for the given key in the given namespace, replacing any
       existing value."""
    log.debug("Storing value for key: %r", key)
    table = _retrieve_table(namespace)
    if table.contains(tinydb.where('key') == key):
        log.debug("Key exists - replacing value")
        table.update({'value': value}, tinydb.where('key') == key)
    else:
        log.debug("Key does not exist - adding")
        table.insert({'key': key, 'value': value})


def retrieve(namespace, key):
    """Retrieve the value stored with a key in the given namespace, or None if
       no value is stored."""
    log.debug("Retrieving value for key: %r", key)
    table = _retrieve_table(namespace)
    element = table.get(tinydb.where('key') == key)
    if element is None:
        log.debug("No value stored")
        return None
    else:
        log.debug("Found value")
        return element['value']


def delete(namespace, key):
    """Delete a key and its value from the store in the given namespace,
       whether it exists or not."""
    log.debug("Deleting value for key: %r", key)
    table = _retrieve_table(namespace)
    table.remove(tinydb.where('key') == key)


def keys(namespace):
    """A list of all keys in the given namespace in the store."""
    log.debug("Listing all stored keys")
    table = _retrieve_table(namespace)
    keys = [element["key"] for element in table.all()]
    return keys
