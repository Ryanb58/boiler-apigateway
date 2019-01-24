import os
import json
from flask import Flask, jsonify, request
from flask_restful import Resource
from flask_jwt_simple import jwt_required, create_jwt
import grpc
from google.protobuf.json_format import MessageToJson

from protos import accounts_pb2
from protos import accounts_pb2_grpc

HOST = os.environ.get('ACCOUNT_SERVICE_HOST', '0.0.0.0')
PORT = str(os.environ.get('ACCOUNT_SERVICE_PORT', '22222'))


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
        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = accounts_pb2_grpc.AccountServiceStub(channel)
            try:
                user = stub.AuthenticateByEmail(
                    accounts_pb2.AuthenticateByEmailRequest(email=email, password=password))
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                print(e)
                return False

        if not user:
            return jsonify({"msg": "Bad email or password"})

        # Identity can be any data that is json serializable
        ret = {'jwt': create_jwt(identity=user.id)}
        return jsonify(ret)


class AccountResource(Resource):

    @jwt_required
    def get(self):
        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = accounts_pb2_grpc.AccountServiceStub(channel)
            try:
                accounts = stub.List(accounts_pb2.ListAccountsRequest(page_size=1, page_token="1"))
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                print(e)
                return False
            return jsonify(json.loads(MessageToJson(accounts)))
