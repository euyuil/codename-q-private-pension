from datetime import date, datetime

from flask import Flask
from flask.json.provider import DefaultJSONProvider

from app.api.routes import api_bp
from app.main.routes import main_bp
from app.models import db
from config import Config

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return super().default(o)

def create_app():
    app = Flask(__name__)
    app.json = UpdatedJSONProvider(app)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')  # API 路由前缀为 /api

    return app
