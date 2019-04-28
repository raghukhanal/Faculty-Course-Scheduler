from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from models import Administrator,Moderator, Faculty, SelectedCourseInfo, Semester, Courses, ClassRoom, DayTime, db
from constants import ROLES

import flask_admin as admin
from flask_admin.contrib.peewee import ModelView

app = Flask(__name__)
app.secret_key = "SomeAwesomeSecret"
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = admin.Admin(app, name="SoftGreen")

admin.add_view(ModelView(Administrator))
admin.add_view(ModelView(Moderator))
admin.add_view(ModelView(Faculty))
admin.add_view(ModelView(SelectedCourseInfo))
admin.add_view(ModelView(Semester))
admin.add_view(ModelView(Courses))
admin.add_view(ModelView(DayTime))


@app.route('/', methods=['POST', 'GET'])
def index_login():
    logged_status = session.get("logged_in")
    if not logged_status:
        return render_template('options_to_login.html')
    else:
        return redirect(url_for("faculty_selection"))


def login(user_id, pin_number, user_role):
    if user_role == ROLES.get("admin"):
        administrator = Administrator.get_or_none(Administrator.user_id == user_id)
        if administrator and (administrator.pin_number == pin_number):
            session['user_id'] = administrator.id
            return True
    elif user_role == ROLES.get("moderator"):
        moderator = Moderator.get_or_none(Moderator.user_id == user_id)
        if moderator and (moderator.pin_number == pin_number):
            session['user_id'] = moderator.id
            return True
    elif user_role == ROLES.get("faculty"):
        faculty = Faculty.get_or_none(Faculty.user_id == user_id)
        if faculty and(faculty.pin_number == pin_number):
            session['user_id'] = faculty.id
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
            flash("You have successfully logged in.")
            return redirect(url_for("admin.index"))
        else:
            flash("Login in failed. Please try again.")
            return redirect(url_for('index_login'))

    return render_template("admin_login.html")


@app.route('/faculty_login', methods=['POST', 'GET'])
def faculty_login():
    if request.method == 'POST':
        form_user = int(request.form.get('user-id'))
        form_pin = int(request.form.get('user-pin'))
        logged_in = login(form_user, form_pin, user_role=ROLES.get("faculty"))
        if logged_in:
            session['logged_in'] = True
            session['role'] = "faulty"
            flash("You have successfully logged in.")
            return redirect(url_for("faculty_selection"))
        else:
            flash("Login in failed. Please try again.")
            return redirect(url_for('index_login'))

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
            flash("You have successfully logged in.")
            return redirect(url_for("moderator_view"))
        else:
            flash("Login in failed. Please try again.")
            return redirect(url_for('index_login'))
    return render_template("moderator_login.html")


@app.route('/moderator_view', methods=['POST', 'GET'])
def moderator_view():
    to_review = SelectedCourseInfo.select()
    return render_template("moderator_view.html", to_review = to_review)


@app.route('/faculty_selection', methods=['POST', 'GET'])
def faculty_selection():
    if request.method == "POST":
        form_term = request.form.get("term_id")
        form_courses = request.form.getlist("course_ids")
        return redirect(url_for("day_time_selection", selected_term=form_term, selected_courses=form_courses))

    courses = Courses.select()
    semester = Semester.select()
    return render_template("selection.html", courses=courses, semester=semester)


@app.route('/select_day_time', methods=['POST', 'GET'])
def day_time_selection():
    if request.method == "POST":
        final_selected = request.form.getlist("selected_course")
        session_user = session.get("user_id")

        for item in final_selected:
            new_record = SelectedCourseInfo.create(faculty_id=session_user, course_id=item)
            try:
                with db.atomic():
                    new_record.save()
                    print(new_record)
            except Exception as e:
                flash("Something went wrong.")
                return redirect(url_for("day_time_selection"))

        flash("Your selected course has been sent to Moderator for review")
        return redirect(url_for("faculty_selection"))

    if request.method == "GET":

        selected_courses = []
        for item in request.args.getlist("selected_courses"):
            selected_courses.append(Courses.get(id=item))
        selected_term = Semester.get(id=request.args['selected_term'])
        return render_template(
            "select_days_and_time.html",
            selected_term=selected_term,
            selected_courses=selected_courses
        )


if __name__ == '__main__':
    app.run(debug=True)
