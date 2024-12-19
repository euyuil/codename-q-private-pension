from .db import db

class BenchmarkConstituent(db.Model):
    """
    Model for benchmark constituent.
    """
    __tablename__ = "benchmark_constituents"

    id = db.Column(db.Integer, primary_key=True)
    benchmark_id = db.Column(db.Integer)
    security_id = db.Column(db.Integer)
    weight = db.Column(db.Float)  # TODO: Decimal???
