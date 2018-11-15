#!/usr/bin/env python
# encoding: utf-8
import web
import json

from config import AUTH

urls = (
    '/api/proxy', 'Proxy',
)

app = web.application(urls, globals())


class Proxy:
    def __init__(self):
        self.proxies = {}

    def POST(self):
        post_data = web.input(_method='post')
        if 'auth' in post_data and post_data['auth'] == AUTH:
            self.proxies[post_data['client_id']] = post_data['data']
            return json.dumps({'code': 0, 'data': self.proxies, 'count': len(self.proxies)})
        else:
            return json.dumps({'code': 1, 'msg': 'Authentication failed'})

    def GET(self):
        get_data = web.input(_method='get')
        if 'auth' in get_data and get_data['auth'] == AUTH:
            return json.dumps({'code': 0, 'data': self.proxies, 'count': len(self.proxies)})
        else:
            return json.dumps({'code': 1, 'msg': 'Authentication failed'})


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
