from flask import Flask, render_template, request, abort, session
from models import Person, Administrator, Faculty, Moderator, Semester, Courses
from constants import ROLES
app = Flask(__name__)
app.secret_key = "SomeAwesomeSecret"


@app.route('/', methods=['POST', 'GET'])
def index_login():
    logged_status = session.get("logged_in")
    return render_template('options_to_login.html')


def login(user_id, pin_number, user_role):
    if user_role == ROLES.get("admin"):
        admin = Administrator.get(Administrator.user_id == user_id)
        if admin and (admin.pin_number == pin_number):
            return True
    elif user_role == ROLES.get("moderator"):
        moderator = Moderator.get(Moderator.user_id == user_id)
        if moderator and (moderator.pin_number == pin_number):
            return True
    elif user_role == ROLES.get("faculty"):
        faculty = Faculty.get(Faculty.user_id == user_id)
        if faculty and (faculty.pin_number == pin_number):
            return True
    else:
        return False


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return index_login()


@app.route('/admin_login', methods=['POST', 'GET'])
def administrator_login():
    if request.method == 'POST':
        form_user = int(request.form.get('user-id'))
        form_pin = int(request.form.get('user-pin'))
        logged_in = login(form_user, form_pin, user_role=ROLES.get("admin"))
        if logged_in:
            session['logged_in'] = True
            session['role'] = "admin"

    return render_template("admin_login.html")


@app.route('/faculty_login', methods=['POST', 'GET'])
def faculty_login():
    if request.method == 'POST':
        form_user = int(request.form.get('user-id'))
        form_pin = int(request.form.get('user-pin'))
        logged_in = login(form_user, form_pin, user_role=ROLES.get("faculty"))
        print("logged in", logged_in)
        if logged_in:
            session['logged_in'] = True
            session['role'] = "faulty"
            return faculty_selection()

    return render_template("faculty_login.html")


@app.route('/moderator_login', methods=['POST', 'GET'])
def moderator_login():
    if request.method == 'POST':
        form_user = int(request.form.get('user-id'))
        form_pin = int(request.form.get('user-pin'))
        logged_in = login(form_user, form_pin, user_role=ROLES.get("moderator"))
        if logged_in:
            session['logged_in'] = True
            session['role'] = "moderator"
    return render_template("moderator_login.html")


@app.route('/faculty_selection', methods=['POST', 'GET'])
def faculty_selection():
    courses = Courses.select()
    semester = Semester.select()
    return render_template("selection.html", courses=courses, semester=semester)


if __name__ == '__main__':
    app.run(debug=True)
