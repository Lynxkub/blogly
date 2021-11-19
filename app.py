from weakref import ProxyTypes
from flask import Flask, render_template, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app=Flask(__name__)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug=DebugToolbarExtension(app)
connect_db(app)

now=datetime.now()


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
    posts=Post.query.filter_by(user_id=user_id).all()
    
    print(user.post)
    return render_template('user_profile.html', user=user, posts=posts)

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

@app.route('/add_post<int:user_id>')
def add_post(user_id):

    user=User.query.get(user_id)
    return render_template('create_post.html', user=user)
    
@app.route('/successful_post_created<int:user_id>', methods=['POST'])
def post_created(user_id):
    user=User.query.get(user_id)
    title=request.form['post_title']
    content=request.form['post_content']
    
    new_post=Post(title=title, content=content, created_at=now, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post Created!')
    return redirect(f'/{user.id}')

@app.route('/post<int:post_id>')
def post_link(post_id):
    post=Post.query.get(post_id)
    time=post.created_at
    readable_time=time.strftime("%d/%m/%Y %H:%M:%S")
    return render_template('post.html', post=post, timestamp=readable_time)


@app.route('/edit_post<int:post_id>')
def edit_post(post_id):
    post=Post.query.get(post_id)

    return render_template('edit_post.html', post=post)

    
@app.route('/submit_edit<int:post_id>', methods=['POST'])
def edit_post_content(post_id):
    edit_post=Post.query.get(post_id)
    title=request.form['edit']
    content=request.form['content_edit']
    created_at=now
    edit_post.title=title
    edit_post.content=content
    edit_post.created_at=created_at
    db.session.add(edit_post)
    db.session.commit()
    flash("Post Edited")
    return redirect('/users')

@app.route('/delete_post<int:post_id>', methods=['POST'])
def delete_post(post_id):
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect('/users')