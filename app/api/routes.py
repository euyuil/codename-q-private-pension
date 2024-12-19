from flask import jsonify, request
from app.api import api_bp
from app.models import db, EnhancedIndexFund, Fund, IndexFund, Security, TargetDateFund
from myutils.bench_util import get_benchmark_data as u_get_benchmark_data

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
    benchmark = Security.query.filter(Security.type.like("TI%")).all()
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
