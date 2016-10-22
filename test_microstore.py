import logging
import unittest
import json

import microstore

CONTENT_TYPE_JSON = 'application/json'


class MicroStoreTestCase(unittest.TestCase):

    def setUp(self):
        # Disable the error catching during request handling so that you get
        # better error reports.
        microstore.app.config['TESTING'] = True
        microstore.kvstore.open()
        self.app = microstore.app.test_client()

    def tearDown(self):
        microstore.kvstore.close()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_apps_collection_empty(self):
        rv = self.app.get('/apps')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), [])

    def test_apps_resource(self):
        app_name = "testapp"
        app_url = '/apps/' + app_name
        data = {"data": {"mykey": "myvalue"}, "name": app_name}

        rv = self.app.put(app_url,
                          data=json.dumps(data),
                          content_type=CONTENT_TYPE_JSON)
        self.assertEqual(rv.status_code, 204)

        rv = self.app.get(app_url)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), data)

    def test_apps_resource_delete(self):
        app_name = "testapp"
        app_url = '/apps/' + app_name
        data = {"data": {"mykey": "myvalue"}, "name": app_name}

        rv = self.app.put(app_url,
                          data=json.dumps(data),
                          content_type=CONTENT_TYPE_JSON)
        self.assertEqual(rv.status_code, 204)

        rv = self.app.get(app_url)
        self.assertEqual(rv.status_code, 200)

        rv = self.app.delete(app_url)
        self.assertEqual(rv.status_code, 204)

        rv = self.app.get(app_url)
        self.assertEqual(rv.status_code, 404)

    def test_apps_collection_populated(self):
        app_name = "testapp"
        app_url = '/apps/' + app_name
        data = {"data": {"mykey": "myvalue"}, "name": app_name}

        rv = self.app.put(app_url,
                          data=json.dumps(data),
                          content_type=CONTENT_TYPE_JSON)
        self.assertEqual(rv.status_code, 204)

        app_name2 = "testapp2"
        app_url2 = '/apps/' + app_name2
        data2 = {"data": {"mykey": "myvalue"}, "name": app_name2}

        rv = self.app.put(app_url2,
                          data=json.dumps(data2),
                          content_type=CONTENT_TYPE_JSON)
        self.assertEqual(rv.status_code, 204)

        rv = self.app.get('/apps')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()),
                         [{"name": app_name}, {"name": app_name2}])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s:%(message)s',
                        level=logging.INFO)
    unittest.main()
