"""
Model for index fund.
"""
from .db import db

class IndexFund(db.Model):
    """
    Model for index fund.
    """
    __tablename__ = "ppf_index_funds"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    is_initiated_fund = db.Column(db.Boolean)
    benchmark_index_id = db.Column(db.Integer)
    benchmark_index_code = db.Column(db.String())
    benchmark_index_name = db.Column(db.String())
    is_etf_linked = db.Column(db.Boolean)
    is_lof = db.Column(db.Boolean)
    management_id = db.Column(db.Integer)
    management_name = db.Column(db.String())
    csrc_ann_date = db.Column(db.Date)
