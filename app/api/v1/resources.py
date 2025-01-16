from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import db
from app.models.tables import Security
from app.api.v1.schemas import SecuritySchema
from app.api.v1.utilities import create_query_from_request_args

security_schema = SecuritySchema()
securities_schema = SecuritySchema(many=True)


class SecurityListResource(Resource):

    def get(self):
        """
        Handle GET requests to /securities
        Lists securities with optional query parameters for filtering, ordering, etc.
        """
        query = create_query_from_request_args(Security, request.args.items())
        securities = query.all()
        return securities_schema.dump(securities), 200

    def post(self):
        """
        Handle POST requests to /securities
        Creates a new security record
        """
        try:
            # Validate and deserialize input
            data = security_schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        security = Security(**data)
        db.session.add(security)
        db.session.commit()
        return security_schema.dump(security), 201


class SecurityResource(Resource):

    def get(self, code):
        """
        Handle GET requests to /securities/<code>
        Retrieves a single security
        """
        security = Security.query.filter_by(code=code).first()
        if not security:
            return {"message": "Security not found"}, 404
        return security_schema.dump(security), 200

    def put(self, code):
        """
        Handle PUT requests to /securities/<code>
        Updates all fields of a security (except `code`)
        """
        security = Security.query.filter_by(code=code).first()
        if not security:
            return {"message": "Security not found"}, 404

        try:
            data = security_schema.load(request.json, partial=("code",))
            # `partial=("code",)` means do not require the 'code' field.
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # We do not allow updating `code`, so skip it:
        # security.code = data.get("code", security.code)

        security.symbol = data.get("symbol", security.symbol)
        security.exchange = data.get("exchange", security.exchange)
        security.type = data.get("type", security.type)
        security.name = data.get("name", security.name)
        security.full_name = data.get("full_name", security.full_name)
        db.session.commit()
        return security_schema.dump(security), 200

    def patch(self, code):
        """
        Handle PATCH requests to /securities/<code>
        Updates specified fields only
        """
        security = Security.query.filter_by(code=code).first()
        if not security:
            return {"message": "Security not found"}, 404

        try:
            # partial=True allows partial updates
            data = security_schema.load(request.json, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # We still don't allow code updates:
        data.pop("code", None)

        for key, value in data.items():
            setattr(security, key, value)

        db.session.commit()
        return security_schema.dump(security), 200

    def delete(self, code):
        """
        Handle DELETE requests to /securities/<code>
        Deletes a security by code
        """
        security = Security.query.filter_by(code=code).first()
        if not security:
            return {"message": "Security not found"}, 404

        db.session.delete(security)
        db.session.commit()
        return "", 204
