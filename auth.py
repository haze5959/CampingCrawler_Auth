from typing import Optional
from fastapi import FastAPI
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import uvicorn

cred = credentials.Certificate("./good-place-camp-accountKey.json")
firebase_admin.initialize_app(cred)
app = FastAPI()


@app.get("/{token}")
def get_user(token: str):
    if token is None:
        # print("Error: No token field provided. Please specify an token.")
        return {'result': False, 'msg': "No token"}

    try:
        decoded_token = auth.verify_id_token(token)
    except firebase_admin._auth_utils.InvalidIdTokenError:
        # print("Error: ID Token is invalid.")
        return {'result': False, 'msg': "ID Token is invalid"}

    uid: str = decoded_token['uid']

    try:
        data = auth.get_user(uid)._data
    except:
        # print("Error: Auth fail.")
        return {'result': False, 'msg': "Auth fail"}

    # print('Successfully fetched user data: {0}'.format(user.uid))

    return {'result': True, 'data': data}


@app.delete("/{token}")
def delete_user(token: str):
    if token is None:
        # print("Error: No token field provided. Please specify an token.")
        return {'result': False, 'msg': "No token"}

    try:
        decoded_token = auth.verify_id_token(token)
    except firebase_admin._auth_utils.InvalidIdTokenError:
        # print("Error: ID Token is invalid.")
        return {'result': False, 'msg': "ID Token is invalid"}

    try:
        uid: str = decoded_token['uid']
    except:
        # print("Error: Auth fail.")
        return {'result': False, 'msg': "Auth fail"}

    auth.delete_user(uid)
    # print('Successfully deleted user')

    return {'result': True, }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
