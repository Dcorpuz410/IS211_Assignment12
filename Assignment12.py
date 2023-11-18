from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize some sample data
students = [
    {'id': 1, 'first_name': 'John', 'last_name': 'Doe'},
    {'id': 2, 'first_name': 'Jane', 'last_name': 'Smith'},
    {'id': 3, 'first_name': 'Alice', 'last_name': 'Johnson'}
]

quizzes = [
    {'id': 1, 'subject': 'Python Basics', 'num_questions': 10, 'date': '2023-05-20'},
    {'id': 2, 'subject': 'Web Development', 'num_questions': 15, 'date': '2023-05-21'}
]

results = []

@app.route('/')
def home():
    return render_template('index.html', students=students, quizzes=quizzes)

@app.route('/results', methods=['POST'])
def save_results():
    student_id = int(request.form['student_id'])
    quiz_id = int(request.form['quiz_id'])
    score = int(request.form['score'])

    # Check if the student and quiz exist
    student_exists = any(student['id'] == student_id for student in students)
    quiz_exists = any(quiz['id'] == quiz_id for quiz in quizzes)

    if not student_exists or not quiz_exists:
        return 'Invalid student or quiz ID'

    # Add the result
    results.append({'student_id': student_id, 'quiz_id': quiz_id, 'score': score})

    return 'Result saved successfully'

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# Define the database models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Initialize the database
db.create_all()

# Initialize some sample data
john = Student(first_name='John', last_name='Smith')
python_quiz = Quiz(subject='Python Basics', num_questions=5, date='2015-02-05')
john_result = Result(student=john, quiz=python_quiz, score=85)

# Add the data to the database
db.session.add(john)
db.session.add(python_quiz)
db.session.add(john_result)
db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# ... Database models and data initialization ...

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if not is_user_logged_in():
        return redirect(url_for('login'))

    # Render the dashboard page
    return render_template('dashboard.html')

def is_user_logged_in():
    # Check if the user is logged in (you can implement your own logic here)
    # For simplicity, we'll use a global variable to track the login state
    return 'logged_in' in session and session['logged_in']

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run()
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# ... Database models and data initialization ...

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... Login functionality ...

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if not is_user_logged_in():
        return redirect(url_for('login'))

    # Fetch the students and quizzes data from the database
    students = Student.query.all()
    quizzes = Quiz.query.all()

    return render_template('dashboard.html', students=students, quizzes=quizzes)

def is_user_logged_in():
    # ... Check if the user is logged in ...

if __name__ == '__main__':
    # ... App configuration and secret key ...

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# ... Database models and data initialization ...

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... Login functionality ...

@app.route('/dashboard')
def dashboard():
    # ... Dashboard functionality ...

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    # Check if the user is logged in
    if not is_user_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = int(request.form['num_questions'])
        date = request.form['date']

        # Create a new quiz object
        new_quiz = Quiz(subject=subject, num_questions=num_questions, date=date)

        # Add the quiz to the database
        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_quiz.html')

def is_user_logged_in():
    # ... Check if the user is logged in ...

if __name__ == '__main__':
    # ... App configuration and secret key ...

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# ... Database models and data initialization ...

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... Login functionality ...

@app.route('/dashboard')
def dashboard():
    # ... Dashboard functionality ...

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    # ... Add Quiz functionality ...

@app.route('/student/<int:id>')
def student_results(id):
    # Check if the user is logged in
    if not is_user_logged_in():
        return redirect(url_for('login'))

    student = Student.query.get(id)

    if not student:
        return 'Student not found'

    quiz_results = Result.query.filter_by(student_id=id).all()

    return render_template('student_results.html', student=student, quiz_results=quiz_results)

def is_user_logged_in():
    # ... Check if the user is logged in ...

if __name__ == '__main__':
    # ... App configuration and secret key ...

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
db = SQLAlchemy(app)

# ... Database models and data initialization ...

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... Login functionality ...

@app.route('/dashboard')
def dashboard():
    # ... Dashboard functionality ...

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    # ... Add Quiz functionality ...

@app.route('/student/<int:id>')
def student_results(id):
    # ... Student Results functionality ...

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    # Check if the user is logged in
    if not is_user_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_id = int(request.form['student'])
        quiz_id = int(request.form['quiz'])
        score = int(request.form['score'])

        # Check if the student and quiz exist
        student = Student.query.get(student_id)
        quiz = Quiz.query.get(quiz_id)

        if not student or not quiz:
            error_message = 'Invalid student or quiz.'
            students = Student.query.all()
            quizzes = Quiz.query.all()
            return render_template('add_result.html', students=students, quizzes=quizzes, error_message=error_message)

        # Create a new result object
        new_result = Result(student_id=student_id, quiz_id=quiz_id, score=score)

        # Add the result to the database
        db.session.add(new_result)
        db.session.commit()

        return redirect(url_for('dashboard'))

    students = Student.query.all()
    quizzes = Quiz.query.all()

    return render_template('add_result.html', students=students, quizzes=quizzes)

def is_user_logged_in():
    # ... Check if the user is logged in ...

if __name__ == '__main__':
    # ... App configuration and secret key ...