from flask import Blueprint, render_template
from baseball_predict_app.src import data_load

# 플라스크
record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('/HITTER/')
def index_HITTER():
    fetch, url_name = data_load.data_select_KBO_HITTER()
    return render_template('record.html', fetch=fetch, url_name=url_name)

@record_bp.route('/PITCHER/')
def index_PITCHER():
    fetch, url_name = data_load.data_select_KBO_PITCHER()
    return render_template('record.html', fetch=fetch, url_name=url_name)
    #return "Pitcher"

@record_bp.route('/DEFENSE/')
def index_DEFENSE():
    fetch, url_name = data_load.data_select_KBO_DEFENSE()
    return render_template('record.html', fetch=fetch, url_name=url_name)
    #return "DEFENSE"

@record_bp.route('/RUNNER/')
def index_RUNNER():
    fetch, url_name = data_load.data_select_KBO_RUNNER()
    return render_template('record.html', fetch=fetch, url_name=url_name)
    #return "RUNNER"