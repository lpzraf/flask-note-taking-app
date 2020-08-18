from flask import (Flask, render_template, request, abort, 
                    redirect, url_for, jsonify,session,g, session)
from flask_modus import Modus
from user import User
from model import db, save_db, user_db, save_user_db
import datetime
import random

app = Flask(__name__)
app.secret_key = 'supermegadupersecretkey'
modus = Modus(app)

date = datetime.datetime.now().strftime('%A, %b %d, %Y')

# notes homepage
@app.route('/notes')
def notes():
    global date
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('notes.html', 
                            date=date,
                            notes=db)

# adding a note
@app.route('/notes/new', methods=["GET", "POST"])
def add_note():
    global date
    if not g.user:
        return redirect(url_for('login'))

    if request.method == "POST":
        note = {"title": request.form['title'],
                "date": request.form['date'],  
                "note_body": request.form['note_body']}
        db.append(note)
        save_db()
        return redirect(url_for('view_note', index=len(db) - 1))
    else:
        return render_template("add_note.html", date=date)

# viewing a note
@app.route('/notes/<int:index>', methods=['GET', 'PATCH', 'DELETE'])
def view_note(index):
    if not g.user:
        return redirect(url_for('login'))

    try:
        note = db[index]
        # if updating a note
        if request.method == b"PATCH":
            note = {"title": request.form['title'],
                "date": request.form['date'],  
                "note_body": request.form['note_body']}
            db[index] = note
            save_db()
            return redirect(url_for('notes'))
        
        # if deleting a note
        if request.method == b"DELETE":
            del note
            save_db()
            return redirect(url_for('notes'))
        
        # if showing a note
        return render_template("note.html", 
                                note=note,
                                index=index,
                                max_index= len(db)-1)
    except IndexError:
        abort(404)

# edit a note
@app.route('/notes/<int:index>/edit')
def edit_note(index):
    if not g.user:
        return redirect(url_for('login'))

    try:
        global date
        note = db[index]
        return render_template("edit.html", 
                                note=note,
                                index=index,
                                max_index= len(db)-1,
                                date=date)
    except IndexError:
        abort(404)

# removing a note 
@app.route('/remove_note/<int:index>', methods=["GET", "POST"])
def remove_note(index):
    if not g.user:
        return redirect(url_for('login'))

    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('notes'))
        else:
            return render_template('remove_note.html', note=db[index])
    except IndexError:
        abort(404)


# session
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        global user_db
        user = [x for x in user_db if x['id'] == session['user_id']][0]
        g.user = user


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in user_db if x['username'] == username][0]
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


# logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global date
    if request.method == 'POST':
        session.pop('user_id', None)
        return redirect(url_for('login'))
    else:
        return render_template('logout.html', date=date)


# profile
@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

# new 
# creating a user
@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    global date
    if request.method == "POST":
        user = {"id": random.randint(0,10000),
                "username": request.form['username'],  
                "password": request.form['password']}
        session['user_id'] = user['id']
        user_db.append(user)
        save_user_db()
        return redirect(url_for("profile"))
    
    return render_template("add_user.html", date=date)


#protected
@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html')
    return redirect(url_for('login'))


# drop session
@app.route('/dropsession')
def dropsession():
    session.pop('user_id', None)
    return 'Dropped!'

