from application import app, session, users, flash, render_template, request, redirect, url_for

@app.route('/')
@app.route('/login')
@app.route('/signin')
@app.route('/sign_in')
@app.route('/home')
def index():
    print(session)
    try:
        if session['activeUser']:
            return redirect(url_for('login'))
    except KeyError:
        redirect('before_first_request')

    return render_template('main/home.html')

@app.route('/logout', methods=['GET', "POST"])
def logout():
    session['activeUser'] = False
    i = 0
    found = False
    while i < len(users) and not found:
        if users[i] == session['username']:
            users.pop(i)
            found = True
        i += 1
    session['username'] = None

    return redirect(url_for('index'))