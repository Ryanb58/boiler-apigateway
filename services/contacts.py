import os
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from flask_restful import reqparse
from flask_jwt_simple import jwt_required, create_jwt
import grpc
from google.protobuf.json_format import MessageToJson

from protos import contacts_pb2
from protos import contacts_pb2_grpc

HOST = os.environ.get('CONTACTS_SERVICE_HOST', '0.0.0.0')
PORT = str(os.environ.get('CONTACTS_SERVICE_PORT', '22222'))

parser = reqparse.RequestParser()


class ContactList(Resource):

    @jwt_required
    def get(self):
        """List out all of the contacts."""
        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = contacts_pb2_grpc.ContactServiceStub(channel)
            try:
                contacts = stub.List(contacts_pb2.ListContactsRequest(page_size=1, page_token="1"))
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                print(e)
                return False
            return jsonify(json.loads(MessageToJson(contacts)))
    @jwt_required
    def post(self):
        """Create a new contact."""
        params = request.get_json()
        group = params.get('group', None)
        firstname = params.get('firstname', None)
        lastname = params.get('lastname', None)
        perfname = params.get('perfname', None)
        email = params.get('email', None)
        phone = params.get('phone', None)
        date_updated = params.get('date_updated', None)
        date_created = params.get('date_created', None)
        author = params.get('author', None)

        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = contacts_pb2_grpc.ContactServiceStub(channel)
            try:
                contact = contacts_pb2.Contact(
                    group=group,
                    firstname=firstname,
                    lastname=lastname,
                    perfname=perfname,
                    email=email,
                    phone=phone,
                    date_updated=date_updated,
                    date_created=date_created,
                    author=author,
                )

                contact = stub.Create(contact)
            except Exception as e:
                print(e)
                raise
            return jsonify(json.loads(MessageToJson(contact)))


class ContactDetail(Resource):

    def get(self, id):
        """Get the details of a single contact."""
        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = contacts_pb2_grpc.ContactServiceStub(channel)
            try:
                contact = stub.GetByID(
                    contacts_pb2.GetByIDContactsRequest(
                        id=id
                    )
                )
            except Exception as e:
                print("Invalid username or password? Or perphaps we couldn't connect?")
                print(e)
                return False
            return jsonify(json.loads(MessageToJson(contact)))

    def put(self, id):
        """Update a specific contact."""
        params = request.get_json(force=True)
        group = params.get('group', None)
        firstname = params.get('firstname', None)
        lastname = params.get('lastname', None)
        perfname = params.get('perfname', None)
        email = params.get('email', None)
        phone = params.get('phone', None)
        date_updated = params.get('date_updated', None)
        date_created = params.get('date_created', None)
        author = params.get('author', None)

        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = contacts_pb2_grpc.ContactServiceStub(channel)
            try:
                contact = contacts_pb2.Contact(
                    id=str(id),
                    group=group,
                    firstname=firstname,
                    lastname=lastname,
                    perfname=perfname,
                    email=email,
                    phone=phone,
                    date_updated=date_updated,
                    date_created=date_created,
                    author=author,
                )

                contact_result = stub.Update(contact)
            except Exception as e:
                print(e)
                raise
            return jsonify(json.loads(MessageToJson(contact_result)))

    def delete(self, id):
        with grpc.insecure_channel(HOST + ':' + PORT) as channel:
            stub = contacts_pb2_grpc.ContactServiceStub(channel)
            try:
                deleteContactRequest = contacts_pb2.DeleteContactRequest(
                    id=id
                )
                contact = stub.Delete(deleteContactRequest)
            except Exception as e:
                print(e)
                raise
            return ''