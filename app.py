from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

DATABASE = 'hw13.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if not first_name or not last_name:
            flash('All fields are required.')
            return render_template('add_student.html')
        conn = get_db_connection()
        conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                     (first_name, last_name))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']
        if not subject or not num_questions or not quiz_date:
            flash('All fields are required.')
            return render_template('add_quiz.html')
        conn = get_db_connection()
        conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                     (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')

@app.route('/student/<int:student_id>')
@login_required
def view_student_results(student_id):
    conn = get_db_connection()
    results = conn.execute('''
        SELECT quizzes.subject, results.score
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    ''', (student_id,)).fetchall()
    conn.close()
    return render_template('view_results.html', results=results)

@app.route('/results/add', methods=['GET', 'POST'])
@login_required
def add_result():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        if not student_id or not quiz_id or not score:
            flash('All fields are required.')
            return render_template('add_result.html', students=students, quizzes=quizzes)
        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                     (student_id, quiz_id, score))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_result.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        # initialize the db if not exists
        with sqlite3.connect(DATABASE) as conn:
            with open('schema.sql') as f:
                conn.executescript(f.read())
            conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                         ('John', 'Smith'))
            conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                         ('Python Basics', 5, '2015-02-05'))
            conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                         (1, 1, 85))
            conn.commit()
    app.run(debug=True)