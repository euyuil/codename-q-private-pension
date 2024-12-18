"""
Model for target date fund.
"""
from .db import db

class TargetDateFund(db.Model):
    """
    Model for target date fund.
    """
    __tablename__ = "ppf_target_date_funds"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    type = db.Column(db.String())
    target_year = db.Column(db.Integer)
    holding_period = db.Column(db.String())
    is_initiated_fund = db.Column(db.Boolean)
    management_id = db.Column(db.Integer)
    management_name = db.Column(db.String())
    csrc_ann_date = db.Column(db.Date)
