from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

students = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    return render_template('student_list.html', students=students.values())

@app.route('/students/add', methods=['GET', 'POST'])
def create_student_form():
    if request.method == 'POST':
        student_id = request.form['id']
        if student_id in students:
            return "Student already exists", 400
        students[student_id] = {
            'id': student_id,
            'name': request.form['name'],
            'age': request.form['age']
        }
        return redirect(url_for('get_students'))
    return render_template('student_form.html', title="Student Details", form_action=url_for('create_student_form'))

@app.route('/students/<student_id>/edit', methods=['GET', 'POST'])
def update_student_form(student_id):
    if request.method == 'POST':
        if student_id not in students:
            return "Student not found", 404
        students[student_id] = {
            'id': student_id,
            'name': request.form['name'],
            'age': request.form['age']
        }
        return redirect(url_for('get_students'))
    return render_template('student_form.html', title="Edit Student", student=students.get(student_id), form_action=url_for('update_student_form', student_id=student_id))

@app.route('/students/<student_id>/delete', methods=['GET'])
def delete_student(student_id):
    if student_id in students:
        del students[student_id]
    return redirect(url_for('get_students'))

if __name__ == "__main__":
    app.run(debug=True)
