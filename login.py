from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "b6b55285733edc8858cb397c17d0ee8e"

USER = {
    "username": 'lucas', "password": '1234'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("User need to be logged to access this page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index_1.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER['username'] and password == USER['password']:
            session['user'] = username
            flash('Login successful!')
            return redirect(url_for('restricted_area'))
        else:
            flash('User or password are invalid.')
            return redirect(url_for("login"))

    return render_template("login_1.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You're out!")
    return redirect(url_for("index"))

@app.route('/restrict_area')
@login_required
def restricted_area():
    return render_template("restricted_1.html", user=session['user'])

if __name__ == '__main__':
    app.run(debug=True)
