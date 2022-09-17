from flask import Flask, render_template, request, flash, session
from scrapper import vacationScraper
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = "super secret key"

picFolder = os.path.join('static','pics')

app.config['UPLOAD_FOLDER'] = picFolder

@app.route("/index")
def index():
    london = os.path.join(app.config['UPLOAD_FOLDER'], 'london.png')
    paris = os.path.join(app.config['UPLOAD_FOLDER'], 'paris.png')
    rome = os.path.join(app.config['UPLOAD_FOLDER'], 'rome.png')
    return render_template("index.html", london=london, paris=paris, rome=rome)

@app.route("/list", methods=["POST", "GET"])
def greet():
    user_name = request.form['name_input']
    checkin = request.form['checkin_input']
    checkout = request.form['checkout_input']
    adults = request.form['adult_input']
    children = request.form['children_input']
    if children == 0:
        children = 'no'
    rooms = request.form['rooms_input']
    message = "Hi " + str(user_name) + "!" + " Welcome to vacationSearch!\nLet's check prices for your vacations for " + adults + " adults and " + children + " children from " + checkin + " to " + checkout + "."
    df = vacationScraper(checkin, checkout, adults, children, rooms)

    return render_template("dateSelection.html", tables=[df.to_html(classes='sortable', index=False)], titles=df.columns.values, message = message)