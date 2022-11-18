from flask import Flask, jsonify, request, Response, send_file
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
# from werkzeug.exceptions import BadRequest
# from urllib.parse import urlparse
import datetime
import csv
import json
app = Flask(__name__)
client = MongoClient('mongodb://172.16.0.67:27017/')
db = client["acculync"]
class ShortLink(Resource):
	def get(self):
		data = request.data
		j = json.loads(data.decode('utf-8'))
		report = j.get('report')
		username = j.get('username')
		startdate = j.get('start_date')
		datestartd = datetime.datetime.strptime(startdate, '%Y-%m-%d')
		enddate = j.get('end_date')
		datestarte = datetime.datetime.strptime(enddate, '%Y-%m-%d')
		l =[['_id', 'username', 'campaign_name','long_url']]
		c = 0
		for d in db["172.16.0.154:11000"].find({'created' :{'$gte':datestartd, '$lt': datestarte}, 'username':username}):
			c +=1
			ab = d['_id'],d['username'],d['campaign_name'],d['long_url']
			l.append(list(ab))
		with open(f'{username}-{startdate}-{enddate}.csv', 'w') as csvfile: 
			csvwriter = csv.writer(csvfile) 
			csvwriter.writerows(l)
		d = {}
		d["price"] =c*2
		d["shortlinks"] = c
		if report == "True":
			return send_file(f'{username}-{startdate}-{enddate}.csv')
		return jsonify(d)

app.add_url_rule('/user/short', view_func=ShortLink.as_view('ShortLink'))
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9002, debug=True)
