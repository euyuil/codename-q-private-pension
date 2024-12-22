import pandas as pd
from flask import abort, render_template
from data_module.data_api import DataManager
from app.main import main_bp
from app.models import EnhancedIndexFund, Fund, IndexFund, Security, TargetDateFund

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

@main_bp.route("/products/funds/<sub_category>/fund/<fund_code>")
def single_fund(sub_category, fund_code):
    """单只基金页面"""
    if sub_category not in ["fof", "indexfunds", "enhanced"]:
        abort(404)
    fund = Fund.query.filter(Fund.code == fund_code).first()
    if not fund:
        abort(404)
    return render_template("products/funds/single_fund.html", sub_category=sub_category, fund=fund)

@main_bp.route("/products/funds/research/indices")
def products_funds_research_indices():
    """基准指数页面"""
    indices = Security.query.filter(Security.type.like("TI%")).all()
    return render_template("products/funds/research/indices.html", indices=indices)

@main_bp.route("/products/funds/research/indices/<index_code>")
def products_funds_research_index_detail(index_code):
    """基准指数详细页面"""
    security = Security.query.filter(Security.code == index_code).first()
    if security is None:
        abort(404, description="No such index found")
    if not security.type.startswith("TI"):
        abort(400, description="This is not an index")
    return render_template("products/funds/research/index_detail.html", security=security)

@main_bp.route("/products/funds/research/managers")
def products_funds_research_managers():
    """基金经理介绍页面"""
    managers = list(get_all_research('managers'))
    return render_template("products/funds/research/managers.html", managers=managers)

@main_bp.route("/products/funds/research/managers/<manager_id>")
def products_funds_research_manager_detail(manager_id):
    """基金经理详细页面"""
    manager = get_research_data('managers', manager_id)
    if not manager:
        abort(404)
    return render_template("products/funds/research/manager_detail.html", manager=manager)

@main_bp.route("/products/funds/research/management")
def products_funds_research_management():
    """管理公司介绍页面"""
    management_companies = list(get_all_research('management'))
    return render_template("products/funds/research/management.html", management_companies=management_companies)

@main_bp.route("/products/funds/research/management/<management_id>")
def products_funds_research_management_detail(management_id):
    """管理公司详细页面"""
    management = get_research_data('management', management_id)
    if not management:
        abort(404)
    return render_template("products/funds/research/management_detail.html", management=management)

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

@main_bp.route("/about")
def about():
    """关于我们页面"""
    return render_template("about.html")
