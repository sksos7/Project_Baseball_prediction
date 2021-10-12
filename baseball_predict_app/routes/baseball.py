from flask import Blueprint, render_template
from baseball_predict_app.src import data_load

# 플라스크
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods = ['GET'])
def index():
    fetch, url_name = data_load.data_select_KBO_RANK()
    return render_template('main.html', fetch=fetch, url_name=url_name)
