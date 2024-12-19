from .db import db

class FundBenchmark(db.Model):
    """
    Model for fund benchmark.
    """
    __tablename__ = "fund_benchmarks"

    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer)
    benchmark_id = db.Column(db.Integer)
    effective_start_date = db.Column(db.Date)
    effective_end_date = db.Column(db.Date)
