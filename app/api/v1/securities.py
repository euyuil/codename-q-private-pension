from typing import List, Tuple
from flask import jsonify, request
from app.api.v1 import api_v1
from app.models import db
from app.models.tables import Security

COMMON_QUERY_PARAMS = ["skip", "take", "orderby"]

def split_args() -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    common_query_args = []
    specific_query_args = []
    for key, value in request.args.items():
        if key in COMMON_QUERY_PARAMS:
            common_query_args.append((key, value))
        else:
            specific_query_args.append((key, value))
    return common_query_args, specific_query_args

@api_v1.route("/securities", methods=["GET"])
def list_securities():
    common_query_args, specific_query_args = split_args()
    query = Security.query
    # TODO: Prevent SQL injection.
    for key_parts_str, value in specific_query_args:
        key_parts = key_parts_str.split(".")
        if len(key_parts) == 1:
            key = key_parts[0]
            query = query.filter(getattr(Security, key) == value)
        elif len(key_parts) == 2:
            key = key_parts[0]
            operator = key_parts[1]
            if operator == "like":
                query = query.filter(getattr(Security, key).like(value))
            elif operator == "startswith":
                query = query.filter(getattr(Security, key).startswith(value))
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        else:
            raise ValueError(f"Unsupported key: {key_parts_str}")
    for key, value in common_query_args:
        if key == "skip":
            query = query.offset(int(value))
        elif key == "take":
            query = query.limit(int(value))
        elif key == "orderby":
            value_parts = value.split(" ")
            if len(value_parts) == 1:
                query = query.order_by(getattr(Security, value))
            elif len(value_parts) == 2:
                key = value_parts[0]
                direction = value_parts[1]
                if direction == "asc":
                    query = query.order_by(getattr(Security, key).asc())
                elif direction == "desc":
                    query = query.order_by(getattr(Security, key).desc())
                else:
                    raise ValueError(f"Unsupported direction: {direction}")
            else:
                raise ValueError(f"Unsupported value: {value}")
        else:
            raise ValueError(f"Unsupported key: {key}")
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
