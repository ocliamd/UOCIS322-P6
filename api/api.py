from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import json_util
import os
import json
import db 


app = Flask(__name__)
api = Api(app)

client = db.Mongodb(os.environ['MONGODB_HOSTNAME'])
client.connect()
client.set_data("brevetsdb")
client.set_collection("latestsubmit")


def _csv(rows):
    h = list(rows[0].keys())
    result = ",".join(h) + "\n"
    for row in rows:
        row_val = [str(r) for r in list(row.values())]
        result += ",".join(row_val) + "\n"
    return result

class listAll(Resource):
    def get(self, data_type=""):
        item = int(request.args.get("top", default=-1))
        fields = ["km", "open", "close"]
        if item > 0:
            rows = client.search_for_head(fields, item)
        elif item == -1:
            rows = client.f_field(fields)
        else:
            return "Need to pass a positive number for top!"
        if len(rows) == 0:
            return "The database has no entries. Please, submit at least 1 control time."
        if data_type == 'csv':
            result = _csv(rows)
        elif data_type == 'json' or data_type == "":
            result = json.loads(json_util.dumps(rows))
        else:
            result = "The data can be displayed in either 'csv' format or 'json' format, choose either 'csv' or 'json'"
        return result


class listOpenOnly(Resource):
    def get(self, data_type=""):
        item = int(request.args.get("top", default=-1))
        fields = ["km", "open"]
        if item > 0:
            rows = client.search_for_head(fields, item)
        elif item == -1:
            rows = client.f_field(fields)
        else:
            return "Need to pass a positive number for top!"
        if len(rows) == 0:
            return "The database has no entries. Please, submit at least 1 control time."
        if data_type == 'csv':
            result = _csv(rows)
        elif data_type == 'json' or data_type == "":
            result = json.loads(json_util.dumps(rows))
        else:
            result = "The data can be displayed in either 'csv' format or 'json' format, choose either 'csv' or 'json'."
        return result


class listCloseOnly(Resource):
    def get(self, data_type=""):
        item = int(request.args.get("top", default=-1))
        fields = ["km", "close"]
        if item > 0:
            rows = client.search_for_head(fields, item)
        elif item == -1:
            rows = client.f_field(fields)
        else:
            return "Must provide a positive number for top!"
        if len(rows) == 0:
            return "The database has no entries. Please, submit at least 1 control time."
        if data_type == 'csv':
            result = _csv(rows)
        elif data_type == 'json' or data_type == "":
            result = json.loads(json_util.dumps(rows))
        else:
            result = "The data can be displayed in either 'csv' format or 'json' format, choose either 'csv' or 'json'."
        return result


#############

# Create routes
api.add_resource(listAll, '/listAll', '/listAll/<string:data_type>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:data_type>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:data_type>')


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
