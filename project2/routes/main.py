from application import app, session, flat, flash, render_template, request, redirect, url_for
from helpers.chatId_enum import ChatId

@app.route('/')
@app.route('/login')
@app.route('/signin')
@app.route('/sign_in')
@app.route('/home')
def index():
    if 'username' in session and 'currentChatId' in session:
        if session['username'] and session['currentChatId']:
            return redirect(url_for('login'))
    else:
        redirect('before_first_request')

    return render_template('main/home.html')

@app.route('/logout', methods=['GET', "POST"])
def logout():
    session['username'] = None
    session['currentChatId'] = ChatId.NONE
    return redirect(url_for('index'))