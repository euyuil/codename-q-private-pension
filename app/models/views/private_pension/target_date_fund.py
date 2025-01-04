"""
Model for target date fund.
"""
from ...db import db

class TargetDateFund(db.Model):
    """
    Model for target date fund.
    """
    __tablename__ = "v_private_pension_target_date_funds"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    type = db.Column(db.String())
    target_year = db.Column(db.Integer)
    holding_period = db.Column(db.String())
    is_initiated_fund = db.Column(db.Boolean)
    management_company_id = db.Column(db.Integer)
    management_company_name = db.Column(db.String())
    csrc_announce_date = db.Column(db.Date)
