print("RUNNING APP.py")
import os
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

import grpc
# import your gRPC bindings here:
from protos import accounts_pb2
from protos import accounts_pb2_grpc

# Import our services:
from services.accounts import AuthenticationResource
from services.accounts import AccountResource

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret-jwt-secret'  # Change this!
jwt = JWTManager(app)

api = Api(app, prefix="/api")


class PrivateResource(Resource):
    @jwt_required
    def get(self):
        return jsonify({'hello_from': get_jwt_identity()})


api.add_resource(AuthenticationResource, '/authorize')
api.add_resource(AccountResource, '/accounts')
api.add_resource(PrivateResource, '/private')

print(__name__)
if __name__ == '__main__':
    LOGGER.info("Starting server.")
    host = os.environ.get('HOST', '0.0.0.0')
    port = str(os.environ.get('PORT', '80'))
    app.run(host=host, port=port, debug=True)
    LOGGER.info("Serving rest-api.")