#step two: the start page
#we'll keep track of the user survey responses with a list

from surveys import satisfaction_survey as survey
RESPONSES = "responses"
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'AAAAA'


debug =  DebugToolbarExtension(app)
#home page route
@app.route('/home-page')
def home_page():
    """Display the homepage, showing the title of the survey
    , the instructions and a button to start."""
    return render_template('home-page.html', survey = survey)

#start the survey
@app.route('/start', methods = ["POST"])
def start_survey():
    """clear the previous responses and start a new blank survey"""
    session[RESPONSES] = []
    return redirect('/questions/0')

#step 4: handle the answers
@app.route('/handle', methods = ['POST'])
def handle_question():
    """Save the curr response and move to the next question, radio."""
    #get the answer
    choice = request.form['answer']

    #append the response to the session
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if(len(responses) == len(survey.questions)):
        #if they fill out the form, move to step 5
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')



#question route
@app.route('/questions/<int:cur>')
def get_questions(cur):
    """Display the first question."""
    responses = session.get(RESPONSES)
    if(responses is None):
        #no response, bring back to homepage
        return redirect('/home-page')
    if(len(responses) == len(survey.questions)):
        #step 5, thank the user
        return redirect('/thank-you')
    if(len(responses) != cur):
        #accessing the questions out of order
        #give a flash message then redirect them out of the page
        flash(f'invalid question order: {cur}')
        return redirect(f'/questions/{len(responses)}')
    question = survey.questions[cur]
    return render_template('get_quest.html', question_num = cur,
    question = question)


#thank you route
@app.route('/thank-you')
def complete_survey():
    """Survey is completed. thank the users"""
    return render_template('thank-you.html')