# microstore

A minimal Python REST microservice datastore, which can be in-memory or JSON file backed.

Runs in-memory only by default, or file-backed if a file name is supplied as a command line argument.

Once running, go to the root URL to explore the API using [Swagger UI](http://swagger.io/swagger-ui/).

## Setup

Relies on [Flask](http://flask.pocoo.org/docs/0.11/) and [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) for the webserver and REST API, and [TinyDB](https://tinydb.readthedocs.io/en/latest/) for the JSON database.

```shell
$ pip install flask flask-restplus tinydb
```

Then just clone or download and extract this repository to get started.

## Running

Run with `-h` for full usage options.

```shell
$ python microstore.py
```

Run the tests by similarly running `python test_microstore.py`.

## Usage

You can explore the API using Swagger UI by opening the base URL (that is printed to the terminal when you run the server) in your web browser - see an example image of this in action below.

In short though, you can `PUT` JSON data to `/apps/<your-app-name-here>` as the `data` key of an object:

```javascript
{
  "data": {
    "any_data": "you_like_here"
  }
}
```

and later retrieve it with a `GET` on the same URL, `DELETE` it, or replace it with another `PUT`.

![Swagger UI example](images/swaggerui.png "Swagger UI example")

## Limitations

- Not production ready. This is designed for simple prototyping use, not performance at huge load and does not meet production security requirements.

- Single threaded. Flask will run single-threaded by default, creating a single synchronous server on a single thread capable of serving only one client at a time, and TinyDB does not support threaded access.

