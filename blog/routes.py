from flask import render_template, request, flash, redirect, url_for
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
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

