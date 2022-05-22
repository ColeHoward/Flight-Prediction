from flask import Blueprint, render_template, url_for, request
import pandas as pd
import numpy as np
from werkzeug.utils import redirect
from flask import current_app as app

rank_bp = Blueprint(
    'rank_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@rank_bp.route('/Rankings', methods=['GET', 'POST'])
def rank():

    return render_template('rank.html')

