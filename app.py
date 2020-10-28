from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = ""

@app.route('/')
def show_survey_start():
  return render_template('start_page.html', survey=survey)




@app.route('/begin', methods=["POST"])
def survey_start():
  session[responses] = []
  return redirect('/questions/0')



@app.route('/answer', methods=["POST"])
def handle_question():

  #Getting the results (if available)
  
  answer = request.form['answer']

  #Adding to the session
  response = session[responses]
  response.append(answer)
  session[responses] = response

  #Directing them to next question or last page
  if (len(response) == len(survey.questions)):
    return redirect('/completed')
  
  else:
    return redirect(f"/questions/{len(response)}")





@app.route('/questions/<int:quesId>')
def question_page(quesId):
  response = session.get(responses)

  if (response is None):
    return redirect('/')

  if (len(response) == len(survey.questions)):
    #Goes to the completion tab
    return redirect('/completed')

  if (len(response) != quesId):
    #Sending error for trying to skip
    flash(f"Invalid question id: {quesId}")
    return redirect(f"/questions/{len(response)}")

  

  question = survey.questions[quesId]
  return render_template('question.html', question_num=quesId, question=question)








@app.route('/completed')
def survey_completed():
  return render_template("completed.html", answers=responses)