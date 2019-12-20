# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:26:01 2019

@author: durga-prasad.kurru
"""

from flask import Flask, jsonify,request,make_response,url_for,redirect
from json import dumps
from requests import post
import json
import ast
from test import OfficeAgent as OA
agent = OA()
app = Flask(__name__)

@app.route('/query', methods=['GET','POST'])

def query():
	global agent
	if request.method == 'GET':
		return make_response('failure')
	if request.method == 'POST':
		req = request.json
		#req = ast.literal_eval(req)
		print(req, type(req))
		query = req['query']
		sender_id = req['sender_id']
		print(query, type(query))
		print(sender_id, type(sender_id))
		return json.dumps(agent.exec_query(query = query, sender_id = sender_id))

@app.route('/heartbeat', methods=['GET','POST'])
def heartbeat():
    if request.method == 'GET':
        return make_response('failure')
    if request.method == 'POST':
        query = request.get_json(force=True)
        print(query, type(query))
        return make_response('success')

if(__name__ == "__main__"):
    #response = agent.exec_query("Hi")
    #print(response)
    app.run(host = '0.0.0.0', port=8000)