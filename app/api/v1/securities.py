from flask import jsonify, request
from app.api.v1 import api_v1
from app.api.v1.utilities import create_query_from_request_args
from app.models import db
from app.models.tables import Security

@api_v1.route("/securities", methods=["GET"])
def list_securities():
    query = create_query_from_request_args(Security, request.args.items())
    securities = query.all()
    return jsonify([
        {
            "code": security.code,
            "symbol": security.symbol,
            "exchange": security.exchange,
            "type": security.type,
            "name": security.name,
            "full_name": security.full_name
        }
        for security in securities
    ])

@api_v1.route("/securities", methods=["POST"])
def create_security():
    security = Security(
        code=request.json["code"],
        symbol=request.json["symbol"],
        exchange=request.json["exchange"],
        type=request.json["type"],
        name=request.json["name"],
        full_name=request.json["full_name"]
    )
    db.session.add(security)
    db.session.commit()
    return jsonify({
        "code": security.code,
        "symbol": security.symbol,
        "exchange": security.exchange,
        "type": security.type,
        "name": security.name,
        "full_name": security.full_name
    }), 201

@api_v1.route("/securities/<code>", methods=["PUT"])
def update_security(code):
    security = Security.query.filter_by(code=code).first()
    # security.code = request.json["code"]
    # TODO: For now we don't allow updating code.
    security.symbol = request.json["symbol"]
    security.exchange = request.json["exchange"]
    security.type = request.json["type"]
    security.name = request.json["name"]
    security.full_name = request.json["full_name"]
    db.session.commit()
    return jsonify({
        "code": security.code,
        "symbol": security.symbol,
        "exchange": security.exchange,
        "type": security.type,
        "name": security.name,
        "full_name": security.full_name
    })

@api_v1.route("/securities/<code>", methods=["PATCH"])
def partial_update_security(code):
    security = Security.query.filter_by(code=code).first()
    #if "code" in request.json:
    #    security.code = request.json["code"]
    if "symbol" in request.json:
        security.symbol = request.json["symbol"]
    if "exchange" in request.json:
        security.exchange = request.json["exchange"]
    if "type" in request.json:
        security.type = request.json["type"]
    if "name" in request.json:
        security.name = request.json["name"]
    if "full_name" in request.json:
        security.full_name = request.json["full_name"]
    db.session.commit()
    return jsonify({
        "code": security.code,
        "symbol": security.symbol,
        "exchange": security.exchange,
        "type": security.type,
        "name": security.name,
        "full_name": security.full_name
    })

@api_v1.route("/securities/<code>", methods=["DELETE"])
def delete_security(code):
    security = Security.query.filter_by(code=code).first()
    db.session.delete(security)
    db.session.commit()
    return "", 204

@api_v1.route("/securities/<code>", methods=["GET"])
def get_security(code):
    security = Security.query.filter_by(code=code).first()
    if security is None:
        return "", 404
    return jsonify({
        "code": security.code,
        "symbol": security.symbol,
        "exchange": security.exchange,
        "type": security.type,
        "name": security.name,
        "full_name": security.full_name
    })

@api_v1.route("/securities/<code>/codes", methods=["GET"])
def list_security_codes(code):
    raise NotImplementedError

@api_v1.route("/securities/<code>/codes", methods=["POST"])
def create_security_code(code):
    raise NotImplementedError

@api_v1.route("/securities/<code>/codes/<alias>", methods=["DELETE"])
def delete_security_code(code, alias):
    raise NotImplementedError
