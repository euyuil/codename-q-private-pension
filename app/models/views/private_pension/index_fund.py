"""
Model for index fund.
"""
from ...db import db

class IndexFund(db.Model):
    """
    Model for index fund.
    """
    __tablename__ = "v_private_pension_index_funds"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    is_initiated_fund = db.Column(db.Boolean)
    tracked_index_id = db.Column(db.Integer)
    tracked_index_code = db.Column(db.String())
    tracked_index_name = db.Column(db.String())
    is_etf_linked = db.Column(db.Boolean)
    is_lof = db.Column(db.Boolean)
    management_company_id = db.Column(db.Integer)
    management_company_name = db.Column(db.String())
    csrc_announce_date = db.Column(db.Date)
