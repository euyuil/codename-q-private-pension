import dataclasses
from datetime import date, datetime
from decimal import Decimal

import simplejson as json
from flask import Flask
from flask.json.provider import JSONProvider

from app.api.routes import api_bp
from app.api.v1 import api_v1_blueprint
from app.main.routes import main_bp
from app.models import db
from config import Config

def custom_serializer(obj):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

class SimpleJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        # Set default parameters or update with any provided kwargs
        kwargs.setdefault("ignore_nan", True)  # Convert NaN to null
        kwargs.setdefault("ensure_ascii", False)  # Allow non-ASCII characters
        kwargs.setdefault("default", custom_serializer)  # Handle custom types
        return json.dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

def create_app():
    app = Flask(__name__)
    app.json = SimpleJSONProvider(app)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")  # API 路由前缀为 /api
    app.register_blueprint(api_v1_blueprint)

    return app
