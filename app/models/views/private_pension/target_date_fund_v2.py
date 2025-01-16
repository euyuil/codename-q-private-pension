"""
Model for target date fund v2.
"""
from ...db import db

class TargetDateFundV2(db.Model):
    """
    Model for target date fund v2.
    """
    __tablename__ = "v_private_pension_target_date_funds_v2"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    symbol = db.Column(db.String())
    exchange = db.Column(db.String())
    name = db.Column(db.String())
    security_type = db.Column(db.String())
    benchmark_id = db.Column(db.Integer)
    benchmark_name = db.Column(db.String())
    fund_type = db.Column(db.String())
    target_year = db.Column(db.Integer)
    holding_period = db.Column(db.String())
    is_initiated_fund = db.Column(db.Boolean)
    management_company_id = db.Column(db.Integer)
    management_company_name = db.Column(db.String())
    csrc_announce_date = db.Column(db.Date)
    effective_start_date = db.Column(db.Date)
    effective_end_date = db.Column(db.Date)
