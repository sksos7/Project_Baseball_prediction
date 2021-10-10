import requests
from bs4 import BeautifulSoup
import sqlite3
from flask import Blueprint, render_template

# 플라스크
record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('/')
def index():
    return render_template('record.html')
