from ..db import db

class FundBenchmark(db.Model):
    """
    Model for view of fund benchmark.
    """
    __tablename__ = "v_fund_benchmarks"

    __table_args__ = (
        db.PrimaryKeyConstraint("fund_id", "benchmark_id", "constituent_id"),
    )

    fund_id = db.Column(db.Integer)
    effective_start_date = db.Column(db.Date)
    effective_end_date = db.Column(db.Date)
    benchmark_id = db.Column(db.Integer)
    benchmark_description = db.Column(db.String)
    constituent_id = db.Column(db.Integer)
    constituent_security_id = db.Column(db.Integer)
    constituent_security_code = db.Column(db.String)
    constituent_weight = db.Column(db.Float)
