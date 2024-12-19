"""
This module contains the model for benchmark.
"""

from .db import db

class Benchmark(db.Model):
    """
    Model for benchmark.
    """
    __tablename__ = "benchmarks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
