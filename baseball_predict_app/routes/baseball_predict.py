from flask import Blueprint, render_template
from baseball_predict_app.src import data_load

# 플라스크
predict_bp = Blueprint('predict', __name__, url_prefix='/predict')

@predict_bp.route('/')
def index():
    predict_record = data_load.data_select_KBO_PREDICT()
    return render_template('predict.html',
                            predict_record=[predict_record.to_html(classes='data', justify='center')],
                            titles=predict_record.columns.values)
