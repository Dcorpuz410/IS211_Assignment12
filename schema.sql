CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE Quizzes (
    quiz_id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date DATE NOT NULL
);

CREATE TABLE StudentResults (
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER,
    PRIMARY KEY (student_id, quiz_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(quiz_id)
);