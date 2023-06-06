from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, Survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "verySecretSurveyKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# =============================================================================
# Global Variables
responses = []
fruits = []

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
    session["responses"] = []
    return redirect("/question")

@app.route("/question", methods=["GET", "POST"])
def get_question_num():
    global num, responses
    num = int(request.args.get("num", 0))

    if num > len(questions):
        flash("Invalid Number.")
        print("Invalid Number.")
        session["responses"] = []
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
                    session["responses"].append(response)
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

# Here is the question in particular from my project's rubric page:
#  "Storing answers in a list on the server has some problems. The biggest one is that there’s only one list – if two people try to answer the survey at the same time, they’ll be stepping on each others’ toes!

# A better approach is to use the session to store response information, so that’s what we’d like to do next. If you haven’t learned about the session yet, move on to step 9 and come back to this later.

# To begin, modify your start page so that clicking on the button fires off a POST request to a new route that will set session[“responses”] to an empty list. The view function should then redirect you to the start of the survey. (This will also take care of the issue mentioned at the end of Step Six.) Then, modify your code so that you reference the session when you’re trying to edit the list of responses."