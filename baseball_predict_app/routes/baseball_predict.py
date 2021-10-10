import requests
from bs4 import BeautifulSoup
import sqlite3
from flask import Blueprint, render_template

# 플라스크
predict_bp = Blueprint('predict', __name__, url_prefix='/predict')

@predict_bp.route('/')
def index():
    return render_template('predict.html')
