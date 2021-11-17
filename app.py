from flask import Flask, render_template, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app=Flask(__name__)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug=DebugToolbarExtension(app)
connect_db(app)


@app.route('/')
def home_page():
    return redirect ('/users')

@app.route('/users')
def users_page():

    users=User.query.all()

    return render_template('users.html', users=users)

@app.route('/users', methods=['POST'])
def new_user_created():
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    url=request.form['profile_picture']

    new_user=User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/new')
def new_user_form():
    return render_template('new_user.html')

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show a single user"""

    user=User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit a users info"""

    user=User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)

@app.route('/delete_user<int:user_id>', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/confirm_edit<int:user_id>', methods=['POST'])
def confirm_edit(user_id):
    """Confirms Edit of Users Info"""

    edit_user=User.query.get(user_id)

    first=request.form['first_name']
    last=request.form['last_name']
    url=request.form['url']

    if first == '':
        flash('Please enter a first name')
    if last == '':
        flash('Please enter a last name')
    if first and last != '':
        edit_user.first_name=first
        edit_user.last_name=last
        edit_user.image_url=url
        db.session.add(edit_user)
        db.session.commit()
        flash('Changes Saved')
    
    return redirect('/users')

    
