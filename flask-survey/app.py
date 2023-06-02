from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, Survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "verySecretSurveyKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# =============================================================================
# Global Variables
responses = []

title = surveys["satisfaction"].title
instructions = surveys["satisfaction"].instructions
questions = surveys["satisfaction"].questions

# =============================================================================
@app.route("/")
def welcome_user():
    return render_template("base.html",
                           title=title,
                           instructions=instructions)

@app.route("/redirect", methods=["GET", "POST"])
def begin_survey():
    return redirect("/question")

@app.route("/question", methods=["GET", "POST"])
def get_question_num():
    global num, responses
    num = int(request.args.get("num", 0))

    if num > len(questions):
        flash("Invalid Number.")
        print("Invalid Number.")
        responses = []
        return redirect("/question")

    if num <= len(questions) - 1:
        if request.form is None:
            pass
        elif request.method == "POST":
            try:
                response = request.form.get("userInput")
                # Prevents user from adding 2 of the same answer when the go back a page.
                if len(responses) >= num and responses[num -1] == response:
                    pass
                else:
                    responses.append(response)
            except:
                pass
        num += 1
        print(responses)
        print(f"num: {num}")
        print(f"The length of questions is: {len(questions)}")
        return render_template("questions.html",
                            title=title,
                            questions=questions,
                            num=num,
                            question=questions[num - 1].question,
                            choices=questions[num - 1].choices)
    elif num >= len(questions):
        return redirect("/thank_you")

@app.route("/thank_you")
def thank_user():
    global num
    print(f"question_number: {num}")
    print(f"The length of questions is: {len(questions)}")
    return render_template("thanks.html")

@app.route("/reset", methods=["GET", "POST"])
def reset_survey():
    global responses, num
    responses = []
    num = 0
    return redirect("/")

# Run the Flask app# =============================================================================
if __name__ == "__main__":
    app.run()


# Get q.Parameter for num in the back end (Sent by front end).
# Need to handle query Parameter.
