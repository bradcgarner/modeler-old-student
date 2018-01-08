# https://courses.thinkful.com/pip-001v3/project/3.3.2
# Hello World in Flask

from flask import Flask
from flask import request, Response, url_for # guessed at this
from os import environ # operating system... how to use .env?
import json

app = Flask(__name__)  # special variable for name of module calling this file


@app.route('/api/initialize', methods=['GET'])
def initialize_get():
  '''return data to initialize app'''
  # fetch from SQL
  # catch error
  response = {
    'etTables': [
      {
        'name': 'string',
        'id': 0
      }
    ],
    'coverings': [
      {
        'name': 'string',
        'id': 0
      }
    ]
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/auth/login', methods=['POST'])
def auth_login_post():
  '''login / create user session'''
  # validate fields
  # fetch user from SQL
  # create auth token
  # catch error
  received = {
    'username': 'string',
    'password': 'string',
  }
  response = {
    'id': 0,
    'username': 'string',
    'authToken': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string',
    'projects': [
      0
    ]
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/users', methods=['POST'])
def users_post():
  '''create new user'''
  # validate fields
  # hash password
  # create new user in SQL
  # return new user with id
  # catch error
  received = {
    'username': 'string',
    'password': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string'
  }
  response = {
    'id': 0,
    'username': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string',
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/users/<id>', methods=['GET'])
def users_get_id(id):
  '''get user by id'''
  # search SQL for user by id
  # return user
  # catch error
  response = {
    'id': 0,
    'username': 'string',
    'authToken': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string',
    'projects': [
      0
    ]
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/users/<id>', methods=['PUT'])
def users_put_id(id):
  '''update user by id'''
  # validate fields
  # update user in SQL
  # return updated user
  # catch errors
  request = {
    'id': 0,
    'username': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string',
    'projects': [
      0
    ]
  }
  response = {
    'id': 0,
    'username': 'string',
    'firstName': 'string',
    'lastName': 'string',
    'organization': 'string',
    'projects': [
      0
    ]
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/projects', methods=['POST'])
def projects_post():
  '''create project'''
  # validate fields
  # create new project in SQL
  # return new project
  # catch errors
  request = {
    'idUser': 0,
    'name': 'string',
    'locationCity': 'string',
    'locationState': 'string',
    'locationCountry': 'string'
  }
  response = {
    'id': 0,
    'name': 'string',
    'locationCity': 'string',
    'locationState': 'string',
    'locationCountry': 'string'
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/projects/<id>', methods=['GET'])
def projects_get_id(id):
  '''get project by id'''
  # search SQL for project by id
  # return found project
    # joined with areas
  # catch errors
  response = {
    'idUser': 0,
    'id': int(id),
    'name': 'string',
    'readMe': 'describe all this...',
    'locationCity': 'string',
    'locationState': 'string',
    'locationCountry': 'string',
    'area': 'sf',
    'volume': 'gallons',
    'thickness': 'inches',
    'areas': [
      {
        'area': 1000,
        'cda': [
          'stringified integer key of other area'
        ],
        'runoff': 'stringified integer key of other area',
        'covering': 'stringified integer key of covering',
        'etTable': 'stringified integer key of et table'
      }
    ],
    'intervalMins': 5,
    'eventGapThreshold': 480,
    'controlledRate': 0.002,
    'controlledHi': 70,
    'controlledLo': 0,
    'source': 'user-input',
    'location': 'Baltimore, MD',
    'startMonth': 'May',
    'startDay': 5,
    'endMonth': 'June',
    'endDay': 15,
    'stormData': [
      0
    ],
    'ranIntervalMins': 5,
    'ranEventGapThreshold': 480,
    'ranControlledRate': 0.002,
    'ranControlledHi': 70,
    'ranControlledLo': 0,
    'ranSource': 'user-input',
    'ranLocation': 'Baltimore, MD',
    'ranStartMonth': 'May',
    'ranStartDay': 5,
    'ranEndMonth': 'June',
    'ranEndDay': 15,
    'ranStormData': [
      0
    ],
    'ranEvents': [
      'string'
    ],
    'analysisStartMonth': 'May',
    'analysisStartDay': 11,
    'analysisEndMonth': 'May',
    'analysisEndDay': 13,
    'analysisStartEvent': 'P2',
    'analysisEndEvent': 'D7'
  }
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/projects/<id>/run', methods=['PUT'])
def projects_run_id(id):
  '''run project calculations by id'''
  request = {
    'userId': 0
  }
  # search project and validate the project matches userId
  # validate that all required project fields are completed
  # run calculations in modeler.py
  # respond with success
  # catch errors
  return Response('success {}'.format(id), 200)

@app.route('/api/projects/<id>', methods=['PUT'])
def projects_put_id(id):
  '''update project by id'''
  # search project and validate the project matches userId
  # check request to see what type of request this is
    # does this matter?
    # except areas?
  # validate data in fields
  # update project in SQL
  # return updated project
    # do we need to worry about joining areas only some of the time?
  # catch errors
  requestRequired = {
    'idUser': 0,
    'id': 0,
  }
  requestGeneral = {
    'name': 'string',
    'readMe': 'describe all this...',
    'locationCity': 'string',
    'locationState': 'string',
    'locationCountry': 'string',
  }
  requestUnits = {
    'area': 'sf',
    'volume': 'gallons',
    'thickness': 'inches',
  }
  requestAreas = {
    'areas': [
      {
        'area': 1000,
        'cda': [
          'stringified integer key of other area'
        ],
        'runoff': 'stringified integer key of other area',
        'covering': 'stringified integer key of covering',
        'etTable': 'stringified integer key of et table'
      }
    ],
  }
  requestIntervals = {
    'intervalMins': 5,
    'eventGapThreshold': 480,
  }
  requestControlled = {
    'controlledRate': 0.002,
    'controlledHi': 70,
    'controlledLo': 0,
  }
  requestStormSettings = {
    'source': 'user-input',
    'location': 'Baltimore, MD',
    'startMonth': 'May',
    'startDay': 5,
    'endMonth': 'June',
    'endDay': 15,
    'stormData': [
      0
    ],
  }
  requestAnalysis = {
    'analysisStartMonth': 'May',
    'analysisStartDay': 11,
    'analysisEndMonth': 'May',
    'analysisEndDay': 13,
    'analysisStartEvent': 'P2',
    'analysisEndEvent': 'D7'
  }
  responseRequired = {
    'idUser': 0,
    'id': 0,
  }
  responseGeneral = {
    'name': 'string',
    'readMe': 'describe all this...',
    'locationCity': 'string',
    'locationState': 'string',
    'locationCountry': 'string',
  }
  responseUnits = {
    'area': 'sf',
    'volume': 'gallons',
    'thickness': 'inches',
  }
  responseAreas = {
    'areas': [
      {
        'area': 1000,
        'cda': [
          'stringified integer key of other area'
        ],
        'runoff': 'stringified integer key of other area',
        'covering': 'stringified integer key of covering',
        'etTable': 'stringified integer key of et table'
      }
    ],
  }
  responseIntervals = {
    'intervalMins': 5,
    'eventGapThreshold': 480,
  }
  responseControlled = {
    'controlledRate': 0.002,
    'controlledHi': 70,
    'controlledLo': 0,
  }
  responseStormSettings = {
    'source': 'user-input',
    'location': 'Baltimore, MD',
    'startMonth': 'May',
    'startDay': 5,
    'endMonth': 'June',
    'endDay': 15,
    'stormData': [
      0
    ],
  }
  responseRanIntervals = {
    'ranIntervalMins': 5,
    'ranEventGapThreshold': 480,
  }
  responseRanControlled = {
    'ranControlledRate': 0.002,
    'ranControlledHi': 70,
    'ranControlledLo': 0,
  }
  responseRanStormSettings = {
    'ranSource': 'user-input',
    'ranLocation': 'Baltimore, MD',
    'ranStartMonth': 'May',
    'ranStartDay': 5,
    'ranEndMonth': 'June',
    'ranEndDay': 15,
    'ranStormData': [
      0
    ],
    'ranEvents': [
      'string'
    ],
  }
  responseAnalysis = {
    'analysisStartMonth': 'May',
    'analysisStartDay': 11,
    'analysisEndMonth': 'May',
    'analysisEndDay': 13,
    'analysisStartEvent': 'P2',
    'analysisEndEvent': 'D7'
  }
  data = json.dumps(responseAnalysis)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/storms/<id>', methods=['GET'])
def storms_get_id(id):
  '''get storm by id'''
  # search SQL for storms by id
  # return found storm
  # catch errors
  response = [0,0,0,0]
  data = json.dumps(response)
  return Response(data, 200, mimetype='application/json')

@app.route('/api/storms', methods=['GET'])
def storms_get_query():
  '''get storms by query parameters'''
  # search storms by query parameters
  # return list of found storms
  # catch errors
  location = request.args.get('location')
  startMonth = request.args.get('startMonth')
  endMonth = request.args.get('endMonth')
  startDay = request.args.get('startDay')
  endDay = request.args.get('endDay')
  data = {
    'location': location,
    'startMonth': startMonth,
    'endMonth': endMonth,
    'startDay': startDay,
    'endDay': endDay,
  }
  response = json.dumps(data)
  return Response(response, 200, mimetype='application/json')

if __name__ == '__main__': # __main__ is name assigned by py if file is run on its own / not called by module
  app.run()  
  # app.run(host=environ['IP'], port=int(environ['PORT']))

# route parameters DONE
# query parameters DONE
# request body DONE
# parse JSON from request body DONE
# format JSON to send in response body DONE

# config - env variables, db path, etc.
# error handling
# authentication

# read from SQL database
# write to SQL database
# create images on server (done)
  # send client url for images so client can access
  # allow user to download images from client
# allow user to download csv