from flask import render_template
from app.main import main_bp
from app.models import EnhancedIndexFund, Fund, IndexFund, Security, TargetDateFund
from data_module.data_api import DataManager
import pandas as pd

data_manager = DataManager()

@main_bp.route("/")
def index():
    """首页"""
    return render_template("index.html")

@main_bp.route("/policy")
def policy():
    """政策解读页面"""
    return render_template("policy.html")

@main_bp.route("/products")
def products():
    """可投产品首页（列出四大类链接）"""
    return render_template("products/index.html")

@main_bp.route("/products/bank")
def products_bank():
    """展示银行理财相关内容"""
    return render_template("products/bank/index.html")

@main_bp.route("/products/bank/list")
def products_bank_list():
    """银行理财的产品列表"""
    return render_template("products/bank/list.html")

@main_bp.route("/products/bank/orgs")
def products_bank_orgs():
    """银行理财的相关机构"""
    return render_template("products/bank/orgs.html")

@main_bp.route("/products/bank/history")
def products_bank_history():
    """银行理财的历史数据"""
    return render_template("products/bank/history.html")

@main_bp.route("/products/deposits")
def products_deposits():
    """展示储蓄存款相关内容"""
    return render_template("products/deposits/index.html")

@main_bp.route("/products/deposits/list")
def products_deposits_list():
    """储蓄存款产品列表"""
    return render_template("products/deposits/list.html")

@main_bp.route("/products/deposits/types")
def products_deposits_types():
    """储蓄存款的定期/活期介绍"""
    return render_template("products/deposits/types.html")

@main_bp.route("/products/deposits/rates")
def products_deposits_rates():
    """储蓄存款的利率比较"""
    return render_template("products/deposits/rates.html")

@main_bp.route("/products/insurance")
def products_insurance():
    """展示商业养老保险相关内容"""
    return render_template("products/insurance/index.html")

@main_bp.route("/products/insurance/list")
def products_insurance_list():
    """商业养老保险的产品列表"""
    return render_template("products/insurance/list.html")

@main_bp.route("/products/insurance/companies")
def products_insurance_companies():
    """商业养老保险的保险公司介绍"""
    return render_template("products/insurance/companies.html")

@main_bp.route("/products/insurance/terms")
def products_insurance_terms():
    """商业养老保险的条款解读"""
    return render_template("products/insurance/terms.html")

@main_bp.route("/products/funds")
def products_funds():
    """公募基金页面"""
    return render_template("products/funds/index.html")

@main_bp.route("/products/funds/fof")
def products_funds_fof():
    """养老FOF页面"""
    funds = TargetDateFund.query.all()
    return render_template("products/funds/fof.html", funds=funds)

@main_bp.route("/products/funds/indexfunds")
def products_funds_indexfunds():
    """指数基金页面"""
    funds = IndexFund.query.all()
    return render_template("products/funds/indexfunds.html", funds=funds)

@main_bp.route("/products/funds/enhanced")
def products_funds_enhanced():
    """增强指数基金页面"""
    funds = EnhancedIndexFund.query.all()
    return render_template("products/funds/enhanced.html", funds=funds)

@main_bp.route("/about")
def about():
    """关于我们页面"""
    return render_template("about.html")

@main_bp.route("/Indices")
def indices():
    indices = Security.query.filter(Security.type.like("TI%")).all()
    return render_template("indices.html", indices=indices)

@main_bp.route("/Indices/<code>")
def sec_index(code):
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
        "sec_index.html",
        security=security,
        dates=dates,
        closing_prices=closing_prices
    )

@main_bp.route("/Funds/<code>")
def fund(code):
    fund = Fund.query.filter(Fund.code == code).first()
    if fund is None:
        return "No such fund found", 404
    return render_template("fund.html", fund=fund)
