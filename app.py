from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'w7301@jqir#'
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

# Home route - Display all students
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
        mysql.connection.commit()
        cur.close()
        flash("Student Added Successfully!")
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", [id])
    student = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s", (name, age, grade, id))
        mysql.connection.commit()
        cur.close()
        flash("Student Updated Successfully!")
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

# Delete student
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Student Deleted Successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
