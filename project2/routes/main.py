from application import app, session, flat, flash, render_template, request, redirect, url_for

@app.route('/')
@app.route('/login')
@app.route('/signin')
@app.route('/sign_in')
@app.route('/home')
def index():
    try:
        if session['activeUser'] and session['user']:
            return redirect(url_for('login'))
    except KeyError:
        redirect('before_first_request')

    return render_template('main/home.html')

@app.route('/logout', methods=['GET', "POST"])
def logout():
    session['activeUser'] = False
    session['user'] = None
    return redirect(url_for('index'))