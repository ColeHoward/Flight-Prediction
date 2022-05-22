from flask import Blueprint, render_template, url_for, request
import pandas as pd
import numpy as np
from werkzeug.utils import redirect
from flask import current_app as app


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')

