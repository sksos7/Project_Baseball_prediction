from flask import Blueprint, render_template
from baseball_predict_app.src import data_load

# 플라스크
result_bp = Blueprint('result', __name__, url_prefix='/result')

@result_bp.route('/')
def index():
    fetch, url_name = data_load.data_select_KBO_RESULT()
    return render_template('result.html', fetch=fetch, url_name=url_name)
