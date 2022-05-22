from flask import Blueprint, render_template, url_for, request, flash
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from werkzeug.utils import redirect
import requests
import time
import math
from flask import current_app as app

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

num_to_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def time_to_minute(time):
    hours, minutes = time.split(':')
    return 60 * int(hours) + int(minutes)


def is_correct_format(input_time):
    try:
        time.strptime(input_time, '%H:%M')
        return True
    except ValueError:
        return False


@home_bp.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        airlines = ['delta air lines', 'jetblue airways', 'air canada', 'southwest airlines', 'westget', 'air transat',
                    'united airlines', 'alaska airlines', 'hawaiian airlines', 'american airlines', 'ua', 'jbu', 'dl',
                    'ac', 'aca', 'ual', 'asa', 'as', 'hal', 'ha', 'aa', 'aal', 'wja', 'tsc', 'ts']

        column_names = ['Scheduled Arrival Time', 'Scheduled Elapsed Time (Minutes)', 'PRCP',
                        'TAVG', 'April', 'August', 'December', 'February', 'January',
                        'July', 'June', 'March', 'May', 'November', 'October', 'September',
                        'ABQ', 'ATL', 'AUS', 'BHM', 'BNA', 'BOI', 'BWI', 'CMH', 'DAL', 'DEN',
                        'ELP', 'HOU', 'IND', 'LAS', 'MCI', 'MDW', 'MKE', 'MSY', 'OAK', 'OKC',
                        'OMA', 'PDX', 'PHX', 'PIT', 'RNO', 'SAT', 'SFO', 'SJC', 'SLC', 'SMF',
                        'STL', 'TPA', 'TUS', 'status']

        prediction_df = pd.DataFrame(columns=column_names[:-1])
        prediction_df.loc[0] = [0 for i in range(len(column_names) - 1)]
        airport = request.form['airport'].lower()
        airline = request.form['airline'].lower()
        arrival_time = request.form['arrival-time']
        takeoff_time = request.form['takeoff-time']

        if not is_correct_format(arrival_time) or not is_correct_format(takeoff_time):
            flash('Please enter arrival time in this format: hour:minute', category="error")
            invalid = "time"
            return render_template('home.html', invalid=invalid)
        if airport not in column_names:
            invalid = "airport"
            flash("Please try another airport or make sure you enter the airport's three letter code",
            category="error")
            return render_template('home.html', invalid=invalid)
        if airline not in airlines:
            invalid = "airline"
            return render_template('home.html', invalid=invalid)
            flash('Please try another airline', category="error", invalid=invalid)

        arrival_min = time_to_minute(arrival_time)
        elapsed_time = arrival_min - time_to_minute(takeoff_time)

        prediction_df['Scheduled Arrival Time'] = arrival_min
        prediction_df['Scheduled Elapsed Time (Minutes)'] = elapsed_time

        # precipitation
        api_key = '511fe526899b1daec72be634b63cd99f'

        # lat and lon for LAX
        input_lat = 33.9416
        input_lon = -118.4085

        lat = str(input_lat)
        lon = str(input_lon)

        api_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon + '&exclude=hourly,daily&appid=' + str(
            api_key)

        response = requests.get(api_url)
        current_weather = response.json()['minutely']

        max_precip = 0

        for tup in current_weather:
            if tup['precipitation'] > max_precip:
                max_precip = tup['precipitation']

        prediction_df['PRCP'] = max_precip

        response = requests.get(api_url)
        current_weather = response.json()['current']

        curr_temp_k = current_weather['temp']

        # convert temp from kelvin to fahrenheit
        curr_temp = int(math.ceil((curr_temp_k - 273.15) * 9 / 5 + 32))
        prediction_df['TAVG'] = curr_temp
        prediction_df[column_names[column_names.index(airport)]] = 1

        url = 'https://flight-prediction-8e469-default-rtdb.firebaseio.com/predictors.json'

        response = requests.get(url)
        response_dict = response.json()

        indexes = []
        col_to_values = {col: [] for col in column_names}
        for index, col_to_val in response_dict.items():
            indexes.append(index)
            for col, val in col_to_val.items():
                col_to_values[col].append(val)
        print('len col_to_values', len(col_to_values))
        print('len indexes', len(indexes))
        data = pd.DataFrame(col_to_values, index=indexes)

        status_to_num = {'Not Delayed': 0, 'Delayed': 1}
        y = data['status'].apply(lambda x: status_to_num[x])
        # X = data.drop('status', axis=1)
        X = data.drop(columns=['status'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        clf = RidgeClassifier().fit(X_train, y_train)
        y_pred = clf.predict(prediction_df)

        if y_pred == 1:
            late = True
        else:
            late = False
        return redirect(url_for('prediction_bp.predict'), late)

    return render_template('home.html')
