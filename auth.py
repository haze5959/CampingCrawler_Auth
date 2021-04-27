import flask
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.Certificate("./good-place-camp-accountKey.json")
firebase_admin.initialize_app(cred)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def get_user():
    if 'token' in request.args:
        id_token = request.args['token']
    else:
        return "Error: No token field provided. Please specify an token."

    try:
        decoded_token = auth.verify_id_token(id_token)
    except firebase_admin._auth_utils.InvalidIdTokenError:
        return "Error: ID Token is invalid."

    uid = decoded_token['uid']

    try:
        user = auth.get_user(uid)
    except:
        return "Error: Auth fail."

    print('Successfully fetched user data: {0}'.format(user.uid))

    return jsonify(user)

@app.route('/', methods=['DELETE'])
def delete_user():
    if 'token' in request.args:
        id_token = request.args['token']
    else:
        return "Error: No token field provided. Please specify an token."

    try:
        decoded_token = auth.verify_id_token(id_token)
    except firebase_admin._auth_utils.InvalidIdTokenError:
        return "Error: ID Token is invalid."

    uid = decoded_token['uid']

    try:
        auth.delete_user(uid)
    except:
        return "Error: Auth fail."

    print('Successfully deleted user')

    return {result: True}


app.run()
