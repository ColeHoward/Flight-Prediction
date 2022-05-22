from flask import Blueprint, render_template, url_for, request
import pandas as pd
import numpy as np
from werkzeug.utils import redirect
from flask import current_app as app
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import json
import math

prediction_bp = Blueprint(
    'prediction_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@prediction_bp.route('/Prediction', methods=['GET', 'POST'])
def predict():

    return render_template('prediction.html')
