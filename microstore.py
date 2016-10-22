'''
A simple REST datastore API, which can be in-memory or JSON file backed.

Runs in-memory only by default, or supply a file with `-f`. Run with `-h` for
full usage options.

Once running, go to the root URL to explore the API using
[swaggerui](http://swagger.io/swagger-ui/).
'''
import logging
import sys
import argparse

from flask import Flask, request
from flask_restplus import Resource, Api, fields

import kvstore


log = logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Simple Datastore API',
          description='A simple REST datastore API')

# Namespace to contain the apps data in the key-value store.
KVSTORE_NAMESPACE_APPS = "apps"

# This collects the API operations into a named group under a root URL.
apps_ns = api.namespace('apps', description='Operations related to app data')


# Specifications of the objects accepted/returned by the API.
App = api.model('App', {
    'name': fields.String(required=True, description='App name'),
})

AppWithData = api.inherit('App with data', App, {
    'data': fields.Raw(required=True, description='App data'),
})


@apps_ns.route('')
class AppsCollection(Resource):
    """ Collection resource containing all apps. """

    @api.marshal_list_with(App)
    def get(self):
        """
        Returns the list of apps.
        """
        log.debug("Listing all apps")
        apps_list = kvstore.keys(KVSTORE_NAMESPACE_APPS)
        return [{'name': app_name} for app_name in apps_list]


@apps_ns.route('/<appid>')
@api.response(404, 'App not found.')
class AppsResource(Resource):
    """ Individual resources representing an app. """

    @api.marshal_with(AppWithData)
    def get(self, appid):
        """
        Returns the data associated with an app.
        """
        log.debug("Getting app: %r", appid)
        app_data = kvstore.retrieve(KVSTORE_NAMESPACE_APPS, appid)
        if app_data is None:
            log.debug("No app found")
            return None, 404
        else:
            log.debug("Found app")
            return {'name': appid, 'data': app_data}

    @api.expect(AppWithData)
    @api.response(204, 'App successfully updated.')
    def put(self, appid):
        """
        Updates an app.
        Use this method to add, or change the data stored for, an app.
        * Send a JSON object with the new data in the request body.

        ```
        {
          "data": {
            "any_data": "you_like_here"
          }
        }
        ```

        * Specify the name of the app to modify in the request URL path.
        """
        log.debug("Updating app: %r", appid)
        kvstore.store(KVSTORE_NAMESPACE_APPS,
                      appid,
                      request.get_json()['data'])
        return None, 204

    @api.response(204, 'App successfully deleted.')
    def delete(self, appid):
        """
        Deletes an app.
        """
        log.debug("Deleting app: %r", appid)
        kvstore.delete(KVSTORE_NAMESPACE_APPS, appid)
        return None, 204


def parse_args(args):
    parser = argparse.ArgumentParser(description='Simple REST Datastore')
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        default=None,
                        help='name of a file to back the database')
    parser.add_argument('--host', metavar='IP', type=str,
                        default=None,
                        help="hostname to listen on - set this to '0.0.0.0' to"
                             " have the server available externally as well. "
                             "Defaults to '127.0.0.1'")
    parser.add_argument('--port', metavar='PORT', type=int,
                        default=None,
                        help='the port of the webserver - defaults to 5000')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args(sys.argv)
    kvstore.init(args.file)
    app.run(host=args.host, port=args.port)
    kvstore.term()
