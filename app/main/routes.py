from flask import render_template, request
from app.main import main_bp
from app.models import db, EnhancedIndexFund, Fund, IndexFund, Security, TargetDateFund
from data_module.data_api import DataManager
import pandas as pd

data_manager = DataManager()

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/Indices')
def indices():
    indices = Security.query.filter(Security.type.like("TI%")).all()
    return render_template('indices.html', indices=indices)

@main_bp.route('/Indices/<code>')
def index(code):
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
        'index.html',
        security=security,
        dates=dates,
        closing_prices=closing_prices
    )

@main_bp.route('/TargetDateFunds')
def target_date_funds():
    funds = TargetDateFund.query.all()
    return render_template('target_date_funds.html', funds=funds)

@main_bp.route('/IndexFunds')
def index_funds():
    funds = IndexFund.query.all()
    return render_template('index_funds.html', funds=funds)

@main_bp.route('/EnhancedIndexFunds')
def enhanced_index_funds():
    funds = EnhancedIndexFund.query.all()
    return render_template('enhanced_index_funds.html', funds=funds)

@main_bp.route("/Funds/<code>")
def fund(code):
    fund = Fund.query.filter(Fund.code == code).first()
    if fund is None:
        return "No such fund found", 404
    return render_template("fund.html", fund=fund)
