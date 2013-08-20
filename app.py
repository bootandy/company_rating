from flask import request
from flask import Flask
from flask import jsonify
from flask.ext.classy import FlaskView
from random import choice
import pymongo


MONGO_SERVER = 'localhost'

app = Flask(__name__)
db = pymongo.Connection(MONGO_SERVER, 27017)['company_perception']


class DataView(FlaskView):
    def index(self):
        return "data lives here"

    # pass in user_id from cookie tracker then user update upsert=true
    def post(self):
        companies = request.json
        if companies:
            db['perceptions'].insert( companies )
        return ''

class AveragesView(FlaskView):
    def post(self):
        company_ids = request.json
        print company_ids
        query_result = db.perceptions.aggregate([{"$match": {"c": {"$in": company_ids}}}, {"$group": {"_id":"$c", "avgx": {"$avg": "$x"}, "avgy": {"$avg": "$y"}}}])

        print query_result['result']
        return jsonify(query_result)


DataView.register(app)
AveragesView.register(app)

if __name__ == '__main__':
    app.debug = True

    if app.config['DEBUG']:
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), 'static')
        })

    app.run()
