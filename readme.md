# microstore

A simple REST datastore microservice, which can be in-memory or JSON file backed.

Runs in-memory only by default, or supply a file to write to as an argument.

Once running, go to the root URL to explore the API using [Swagger UI](http://swagger.io/swagger-ui/).

## Setup

Relies on `flask`, `flask-restplus`, and `tinydb`

```shell
$ pip install flask flask-restplus tinydb
```

Then just clone or download and extract this repository.

## Running

Run with `-h` for full usage options.

```shell
python microstore.py
```
