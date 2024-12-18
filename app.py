from flask import Flask, jsonify, request, render_template
from flask.json.provider import DefaultJSONProvider
from datetime import date, datetime
from config import Config
from models import db, EnhancedIndexFund, IndexFund, Security, TargetDateFund
from data_module.data_api import DataManager
import pandas as pd

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def create_app():
    app = Flask(__name__)
    app.json = UpdatedJSONProvider(app)
    app.config.from_object(Config)
    db.init_app(app)

    #with app.app_context():
    #    db.create_all()
    data_manager = DataManager()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/Indices')
    def indices():
        indices = Security.query.filter(Security.type.like("TI%")).all()
        return render_template('indices.html', indices=indices)

    @app.route('/Indices/<code>')
    def index_(code):
        security = Security.query.filter(Security.code == code).first()
        if security is None:
            return "No such index found", 404
        if security.type[:2] != "TI":
            return "This is not an index", 400
        code = security.code

        index_data = data_manager.get_data(
            start="2024-01-01",
            end="2024-12-31",
            frequency="1d",
            securities=[code],
            fields=["Close"]
        )

        dates = [date.strftime("%Y-%m-%d") for date in pd.to_datetime(index_data.datetime)]
        closing_prices = [price.item() for price in index_data["Close"].values]

        return render_template(
            'index_.html',
            security=security,
            dates=dates,
            closing_prices=closing_prices
        )

    @app.route('/TargetDateFunds')
    def target_date_funds():
        funds = TargetDateFund.query.all()
        return render_template('target_date_funds.html', funds=funds)

    @app.route('/IndexFunds')
    def index_funds():
        funds = IndexFund.query.all()
        return render_template('index_funds.html', funds=funds)

    @app.route('/EnhancedIndexFunds')
    def enhanced_index_funds():
        funds = EnhancedIndexFund.query.all()
        return render_template('enhanced_index_funds.html', funds=funds)

    @app.route("/api/targetDateFunds", methods=["GET"])
    def get_target_date_funds():
        target_date_funds = TargetDateFund.query.all()
        return jsonify(
            [
                {
                    "id": fund.id,
                    "code": fund.code,
                    "name": fund.name,
                    "type": fund.type,
                    "target_year": fund.target_year,
                    "holding_period": fund.holding_period,
                    "is_initiated_fund": fund.is_initiated_fund,
                    "amc_id": fund.amc_id,
                    "amc_name": fund.amc_name,
                    "csrc_ann_date": fund.csrc_ann_date
                }
                for fund in target_date_funds
            ]
        )

    @app.route("/api/indexFunds", methods=["GET"])
    def get_index_funds():
        index_funds = IndexFund.query.all()
        return jsonify(
            [
                {
                    "id": fund.id,
                    "code": fund.code,
                    "name": fund.name,
                    "is_initiated_fund": fund.is_initiated_fund,
                    "benchmark_index_id": fund.benchmark_index_id,
                    "benchmark_index_code": fund.benchmark_index_code,
                    "benchmark_index_name": fund.benchmark_index_name,
                    "is_etf_linked": fund.is_etf_linked,
                    "is_lof": fund.is_lof,
                    "amc_id": fund.amc_id,
                    "amc_name": fund.amc_name,
                    "csrc_ann_date": fund.csrc_ann_date
                }
                for fund in index_funds
            ]
        )

    @app.route("/api/enhancedIndexFunds", methods=["GET"])
    def get_enhanced_index_funds():
        enhanced_index_funds = EnhancedIndexFund.query.all()
        return jsonify(
            [
                {
                    "id": fund.id,
                    "code": fund.code,
                    "name": fund.name,
                    "is_initiated_fund": fund.is_initiated_fund,
                    "benchmark_index_id": fund.benchmark_index_id,
                    "benchmark_index_code": fund.benchmark_index_code,
                    "benchmark_index_name": fund.benchmark_index_name,
                    "is_lof": fund.is_lof,
                    "amc_id": fund.amc_id,
                    "amc_name": fund.amc_name,
                    "csrc_ann_date": fund.csrc_ann_date
                }
                for fund in enhanced_index_funds
            ]
        )

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
