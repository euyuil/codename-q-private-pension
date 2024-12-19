from .db import db

class Fund(db.Model):
    """
    Model for fund.
    """
    __tablename__ = "funds"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())
    management_id = db.Column(db.Integer)
    type = db.Column(db.String())
    custodian_id = db.Column(db.Integer)
    management_fee = db.Column(db.Float)
    custodian_fee = db.Column(db.Float)
    sales_service_fee = db.Column(db.Float)
    value_added_service_fee = db.Column(db.Float)
    is_initiated_fund = db.Column(db.Boolean)
    is_fof = db.Column(db.Boolean)
    is_etf_linked = db.Column(db.Boolean)
    is_lof = db.Column(db.Boolean)
