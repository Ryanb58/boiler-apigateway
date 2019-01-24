import os

from flask import Flask, jsonify, request
from flask_restful import Resource
from flask_jwt_simple import jwt_required, create_jwt
import grpc

from protos import accounts_pb2
from protos import accounts_pb2_grpc

HOST = os.environ.get('ACCOUNT_SERVICE_HOST', '0.0.0.0')
PORT = str(os.environ.get('ACCOUNT_SERVICE_PORT', '22222'))

class User(object):
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

    def __str__(self):
        return "User(id={}, email={}, name={})".format(self.id, self.email, self.name)

    def identity(payload):
        user_id = payload['identity']
        return {"user_id": user_id}

class AuthenticationResource(Resource):
    def post(self):
        # Provide a method to create access tokens. The create_jwt()
        # function is used to actually generate the token
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})

        params = request.get_json()
        email = params.get('email', None)
        password = params.get('password', None)

        if not email:
            return jsonify({"msg": "Missing email parameter"})
        if not password:
            return jsonify({"msg": "Missing password parameter"})

        # Verify the email/password.

        with grpc.insecure_channel(host + ':' + port) as channel:
            stub = accounts_pb2_grpc.AccountServiceStub(channel)
            try:
                authenticated = stub.AuthenticateByEmail(
                    accounts_pb2.AuthenticateByEmailRequest(email=email, password=password))
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                return False

        if authenticated:
            return User(id=authenticated.id)

        user = verify(email, password)
        if not user:
            return jsonify({"msg": "Bad email or password"})

        # Identity can be any data that is json serializable
        ret = {'jwt': create_jwt(identity=user.id)}
        return jsonify(ret)


class AccountResource(Resource):
    @jwt_required
    def get(self):
        with grpc.insecure_channel(host + ':' + port) as channel:
            stub = accounts_pb2_grpc.AccountServiceStub(channel)
            try:
                authenticated = stub.AuthenticateByEmail(
                    accounts_pb2.AuthenticateByEmailRequest(email=email, password=password))
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                return False
