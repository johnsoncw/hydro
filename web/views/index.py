from flask import render_template


def index():
    water_t=45
    air_t=75
    return render_template('home.html', water_temp=water_t, air_temp=air_t)
