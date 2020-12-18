from flask import render_template, request, flash, redirect, url_for, session
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def entry(entry_id=None):
    if entry_id is None:
        form = EntryForm()
        errors = None
        if request.method == "POST":
            if form.validate_on_submit():
                entry = Entry(
                    title = form.title.data,
                    body = form.body.data,
                    is_published = form.is_published.data
                )
                db.session.add(entry)
                db.session.commit()
                flash(f'Dodano wpis {form.title.data} do bloga!')
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)
    else:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
                flash(f'Zmieniono wpis {form.title.data}')
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/drafts/', methods=['GET', 'POST'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)
    
@app.route("/drafts-entry/<int:entry_id>", methods=["GET", "POST"])
@login_required
def delete_entry(entry_id=None):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    db.session.delete(entry)
    db.session.commit()
    flash(f'Usuniętio wpis {form.title.data}')
    return redirect(url_for("list_drafts"))

@app.route("/delete-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def delete_post(entry_id=None):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    # form = EntryForm(obj=entry)
    db.session.delete(entry)
    db.session.commit()
    # flash(f'Usuniętio wpis {form.title.data}')
    return redirect(url_for("index"))






