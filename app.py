from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import flash
from flask import session
from user import add_new_user, login_user, fetch_user
from admin import admin_check, user_list, update_user, delete_user
from meetings import add_meeting, fetch_meetings, fetch_meeting, update_meeting, delete_meeting

app = Flask(__name__)
app.secret_key = "oksubho"


@app.route('/')
def home():
    try:
        if session['user'] and session['login']:
            return redirect('/dashboard')
        else:
            session['login'] = False
            session['user'] = None
            return render_template('index.html')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/register/verify', methods=['GET', 'POST'])
def register_verify():
    confirmation = add_new_user(dict(request.form))
    if confirmation == 'Registered user successfully':
        flash(confirmation, 'success')
        return redirect('/login')
    else:
        flash(confirmation, 'error')
        return redirect('/register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['login'] and session['user']:
            return redirect('/dashboard')
        else:
            return render_template('login.html')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return render_template('login.html')


@app.route('/login/verify', methods=['GET', 'POST'])
def login_verify():
    if request.method == 'POST':
        confirmation = login_user(dict(request.form))
        if confirmation == 'Logged in successfully':
            flash(confirmation, 'success')
            return redirect('/dashboard')
        else:
            flash(confirmation, 'error')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/dashboard')
def dashboard():
    try:
        if session['user'] and session['login']:
            user = fetch_user(session['user'])
            return render_template('dashboard.html', user=user, meetings=fetch_meetings(),
                                   admin=admin_check(session['user']))
        else:
            return redirect('/login')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    session['login'] = False
    return redirect('/login')


@app.route('/participants', methods=['GET', 'POST'])
def participants():
    try:
        if session['user'] and session['login']:
            return render_template('user_list.html', participants=user_list(), admin=admin_check(session['user']))
        else:
            return redirect('/login')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return redirect('/login')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                return render_template('admin.html')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return redirect('/login')


@app.route('/u/<id>')
def user_page(id):
    try:
        if session['user'] and session['login']:
            user = fetch_user(id.lower())
            return render_template('user.html', user=user, admin=admin_check(session['user']))
        else:
            return redirect('/login')
    except KeyError:
        session['login'] = False
        session['user'] = None


@app.route('/u/<id>/edit')
def edit_user(id):
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                return render_template('edit_user.html', user=fetch_user(id.lower()))
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['login'] = False
        session['user'] = None
        return redirect('/login')


@app.route('/u/<id>/edit/submit', methods=['GET', 'POST'])
def submit_edit(id):
    if request.method == 'POST':
        flash(update_user(id, request.form))
        return redirect(f'/u/{id.lower()}')
    else:
        return redirect('/')


@app.route('/u/<id>/delete')
def remove_user(id):
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                flash(delete_user(id))
                return redirect('/participants')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings')
def meetings_list():
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                return render_template('meetings.html', meetings=fetch_meetings())
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings/add')
def new_meeting():
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                return render_template('add_meeting.html')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings/add/submit', methods=['GET', 'POST'])
def new_meeting_add():
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                if request.method == "POST":
                    data = request.form
                    flash(add_meeting(dict(data)))
                    return redirect('/admin/meetings')
                else:
                    return redirect('/admin/meetings')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings/<meeting_id>/edit')
def edit_meeting(meeting_id):
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                return render_template('edit_meeting.html', meeting=fetch_meeting(meeting_id))
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings/<meeting_id>/edit/submit', methods=['GET', 'POST'])
def edit_meeting_submit(meeting_id):
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                if request.method == 'POST':
                    flash(update_meeting(meeting_id, dict(request.form)))
                    return redirect('/admin/meetings')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


@app.route('/admin/meetings/<id>/delete')
def remove_meeting(id):
    try:
        if session['user'] and session['login']:
            if admin_check(session['user']):
                flash(delete_meeting(int(id)))
                return redirect('/admin/meetings')
            else:
                return render_template('unauth_access.html')
        else:
            return redirect('/login')
    except KeyError:
        session['user'] = None
        session['login'] = False
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
