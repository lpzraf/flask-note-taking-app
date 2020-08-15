from flask import (Flask, render_template, request, abort, 
                    redirect, url_for, jsonify,session,g)
from flask_modus import Modus
from model import db, save_db
import datetime


app = Flask(__name__)
app.secret_key = 'supermegadupersecretkey'
modus = Modus(app)

# session
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

# notes homepage
@app.route('/notes')
def notes():
    date = datetime.datetime.now().strftime('%A, %b %d, %Y')
    return render_template('notes.html', 
                            date=date,
                            notes=db)

# adding a note
@app.route('/notes/new', methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        note = {"title": request.form['title'],
                "date": request.form['date'],  
                "note_body": request.form['note_body']}
        db.append(note)
        save_db()
        return redirect(url_for('view_note', index=len(db) - 1))
    else:
        return render_template("add_note.html")

# viewing a note
@app.route('/notes/<int:index>', methods=['GET', 'PATCH', 'DELETE'])
def view_note(index):
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
    try:
        note = db[index]
        return render_template("edit.html", 
                                note=note,
                                index=index,
                                max_index= len(db)-1)
    except IndexError:
        abort(404)

# removing a note 
@app.route('/remove_note/<int:index>', methods=["GET", "POST"])
def remove_note(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('notes'))
        else:
            return render_template('remove_note.html', note=db[index])
    except IndexError:
        abort(404)

class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Rafa', password='password'))
users.append(User(id=2, username='Cristina', password='password2'))
users.append(User(id=3, username='Kelly', password='password3'))


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

# profile
@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')
