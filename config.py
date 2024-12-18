import os

class Config:
    # PostgreSQL 数据库连接字符串格式：
    # postgresql://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # 用于会话安全，实际使用中请更换
