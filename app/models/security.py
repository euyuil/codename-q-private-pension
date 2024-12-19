"""
Model for security.
"""
from .db import db

class Security(db.Model):
    """
    Model for security.
    """
    __tablename__ = "securities"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    symbol = db.Column(db.String())
    exchange = db.Column(db.String())
    type = db.Column(db.String())
    short_name = db.Column(db.String())
    full_name = db.Column(db.String())
