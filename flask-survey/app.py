from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, Survey, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = "verySecretSurveyKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def app_page():
    return render_template("base.html")