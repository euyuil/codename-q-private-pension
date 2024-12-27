from datetime import datetime

import pandas as pd
from flask import jsonify, request
from data_module.data_api import DataManager
from app.api import api_bp
from app.models import views, EnhancedIndexFund, IndexFund, TargetDateFund
from myutils.bench_util import get_benchmark_data as u_get_benchmark_data
from myutils import eval_util

data_manager = DataManager()

@api_bp.route("/funds/research/indices/<index_code>/data")
def api_funds_research_index_data(index_code):
    """API: 获取基准指数的行情数据"""
    security = views.Security.query.filter(views.Security.code == index_code).first()
    if security is None:
        return jsonify({"error": "No such index found"}), 404
    if not security.type.startswith("TI"):
        return jsonify({"error": "This is not an index"}), 400
    code = security.code

    try:
        index_data = data_manager.get_data(
            start="1980-01-01",
            end=datetime.now(),
            frequency="1d",
            securities=[code],
            fields=["AdjClose"]
        )
    except Exception as e:
        return jsonify({"error": "Failed to retrieve index data", "message": str(e)}), 500

    if len(index_data) == 0 or "AdjClose" not in index_data.data_vars:
        return jsonify({"error": "No data available for the given index"}), 404

    dates = [date.strftime("%Y-%m-%d") for date in pd.to_datetime(index_data.datetime)]
    closing_prices = [price.item() for price in index_data["AdjClose"].values]

    return jsonify({
        "dates": dates,
        "closing_prices": closing_prices
    })

@api_bp.route("/targetDateFunds", methods=["GET"])
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

@api_bp.route("/indexFunds", methods=["GET"])
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

@api_bp.route("/enhancedIndexFunds", methods=["GET"])
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

@api_bp.route("/benchmark", methods=["GET"])
def get_benchmark():
    benchmark = views.Security.query.filter(views.Security.type.like("TI%")).all()
    return jsonify(
        [
            {
                "id": index.id,
                "code": index.code,
                "name": index.name,
                "type": index.type
            }
            for index in benchmark
        ]
    )

@api_bp.route("/benchmarkData", methods=["GET"])
def get_benchmark_data():
    fund_id = request.args.get("fund_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    benchmark_data = u_get_benchmark_data(fund_id, start_date, end_date)
    return jsonify(benchmark_data)

@api_bp.route("/securities/<code>/performance", methods=["GET"])
def get_security_performance(code):
    security = views.Security.query.filter(views.Security.code == code).first()
    if security is None:
        return jsonify({"error": "No such security found"}), 404
    if security.type not in ["TIE", "TID"]:
        return jsonify({"error": "This is not an equity security"}), 400

    try:
        ds = data_manager.get_data(
            start="1980-01-01",
            end=datetime.now(),
            frequency="1d",
            securities=[code],
            fields=["AdjClose"]
        )
    except Exception as e:
        return jsonify({"error": "Failed to retrieve security data", "message": str(e)}), 500

    if len(ds) == 0 or "AdjClose" not in ds.data_vars:
        return jsonify({"error": "No data available for the given security"}), 404

    da = ds["AdjClose"]
    results = eval_util.get_evaluation_results(da)
    return jsonify(results)
