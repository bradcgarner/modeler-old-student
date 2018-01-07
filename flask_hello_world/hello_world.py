# https://courses.thinkful.com/pip-001v3/project/3.3.2
# Hello World in Flask

from flask import Flask
from flask import request, Response, url_for # guessed at this
from os import environ # operating system... how to use .env?
import json

app = Flask(__name__)  # special variable for name of module calling this file


@app.route('/api/posts', methods=['GET'])
def posts_get():
  '''get a list of posts'''
  data = json.dumps({'a':['a','b'],'x':{'b':'c'}})
  return Response(data, 200, mimetype='application/json')

@app.route('/api/posts', methods=['POST'])
def posts_post():
  ''' accept json body and print'''
  data = request.json
  return Response(json.dumps(data), 200, mimetype='application/json')

@app.route('/api/posts/route/<route>')
def echo_route(route):
  return 'Hello from route/{}!'.format(route.title())

@app.route('/api/posts/query', methods=['GET'])
def posts_get_query():
  ''' accept query strings and print'''
  data = request.args.get('title_like')
  print(data)
  return Response(json.dumps(data), 200, mimetype='application/json')


@app.route('/')
@app.route('/hello')
def say_hi():
  return 'Hello World!'

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