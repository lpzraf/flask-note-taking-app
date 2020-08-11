from flask import Flask, render_template, request, abort, redirect, url_for, jsonify
from model import db, save_db
import datetime


app = Flask(__name__)

# homepage
@app.route('/')
def homepage():
    date = datetime.datetime.now().strftime('%A, %b %d, %Y')
    return render_template('homepage.html', 
                            date=date,
                            notes=db)

# adding a note
@app.route('/add_note', methods=["GET", "POST"])
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
@app.route('/notes/<int:index>')
def view_note(index):
    try:
        note = db[index]
        return render_template("note.html", 
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
            return redirect(url_for('homepage'))
        else:
            return render_template('remove_note.html', note=db[index])
    except IndexError:
        abort(404)

# @app.route('/api/note/')
# def api_note_list():
#     return jsonify(db)

# @app.route('/api/note/<int:index>')
# def api_note_detail(index):
#     try:
#         return db[index]
#     except IndexError:
#         abort(404)
