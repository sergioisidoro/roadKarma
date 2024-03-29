from flask import Flask, render_template, Response, request
import redis
import logging
import json
try:
    from flask_cors import cross_origin
    # support local usage without installed package
except:
    from flask.ext.cors import cross_origin
    # this is how you would normally import


app = Flask(__name__, static_folder='./static', static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
red = redis.StrictRedis()


def event_stream(channel):
    pubsub = red.pubsub()
    pubsub.subscribe(channel)
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']


@app.route('/goodGuy', methods=['GET', 'POST', 'OPTIONS'])
def index1():
    dirver_id = 123
    badGuy_id = 234
    return render_template('index.html', **locals())

@app.route('/badGuy', methods=['GET', 'POST', 'OPTIONS'])
def index2():
    dirver_id = 234
    return render_template('index.html', **locals())

@app.route('/driver1', methods=['GET', 'POST', 'OPTIONS'])
def index3():
    dirver_id = 345
    return render_template('index.html', **locals())

@app.route('/driver2', methods=['GET', 'POST', 'OPTIONS'])
def index4():
    dirver_id = 456
    return render_template('index.html', **locals())

@app.route('/app/sendWTF/<tagID>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['GET', 'POST', 'OPTIONS'], headers=['X-Requested-With', 'Content-Type', 'Origin', 'withCredentials', 'Access-Control-Allow-Credentials', 'token'])
def fuck(tagID):
    logging.warning('Recieved Fuck you! to ' + tagID )
    requester = request.form['sender_id']
    message = json.dumps({'sender_id': requester , 'message': "WTF!!!"})
    logging.warning('From ' + requester )
    red.publish(tagID, message)
    return Response(status=202)


@app.route('/app/sendThanks/<tagID>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['GET', 'POST', 'OPTIONS'], headers=['X-Requested-With', 'Content-Type', 'Origin', 'withCredentials', 'Access-Control-Allow-Credentials', 'token'])
def thanks(tagID):
    requester = request.form['sender_id']
    message = json.dumps({'sender_id': requester , 'message': "Thanks :)"})
    logging.warning('Recieved Thank you! to ' + tagID)
    red.publish(tagID, message)
    return Response(status=202)


@app.route('/app/sendSorry/<tagID>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['GET', 'POST', 'OPTIONS'], headers=['X-Requested-With', 'Content-Type', 'Origin', 'withCredentials', 'Access-Control-Allow-Credentials', 'token'])
def sorry(tagID):
    requester = request.form['sender_id']
    message = json.dumps({'sender_id': requester , 'message': "Sorry =/"})
    logging.warning('Recieved Sorry! to ' + tagID)
    red.publish(tagID, message)
    return Response(status=202)


@app.route('/app/sendMessage/<tagID>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['GET', 'POST', 'OPTIONS'], headers=['X-Requested-With', 'Content-Type', 'Origin', 'withCredentials', 'Access-Control-Allow-Credentials', 'token'])
def message(tagID):
    message = request.json['message']
    logging.warning('Recieved message ' + message + ' to ' + tagID)
    red.publish(tagID, message)
    return Response(status=202)


@app.route('/app/listen/<tagID>')
@cross_origin(origins='*', methods=['GET', 'POST', 'OPTIONS'], headers=['X-Requested-With', 'Content-Type', 'Origin', 'withCredentials', 'Access-Control-Allow-Credentials', 'token'])
def stream(tagID):
    print "Connection started"
    resp = Response(event_stream(tagID), mimetype="text/event-stream")
    print resp
    return resp

if __name__ == "__main__":
    app.debug = True
    app.config.from_pyfile('config.py')
    logging.warning('\n\n')
    logging.warning('       (  ( ( . ) )  )')
    logging.warning('              |      ')
    logging.warning('          listening...     ')
    logging.warning('\n\n')
    app.run(host='0.0.0.0', port=3000)

