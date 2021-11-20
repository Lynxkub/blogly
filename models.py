from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app=app
    db.init_app(app)

class User(db.Model):
    """User creation/deletion"""

    __tablename__='users'

    id=db.Column(db.Integer,
                primary_key=True,
                autoincrement = True)

    first_name = db.Column(db.String,
                            nullable = False)

    last_name = db.Column(db.String,
                            nullable = False)

    image_url = db.Column(db.String)


class Post(db.Model):
    """Users Created Posts"""

    __tablename__='posts'

    id=db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    title=db.Column(db.Text,
                    nullable=False)
    
    content=db.Column(db.Text,
                    nullable=False)
    
    created_at=db.Column(db.DateTime)

    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))

    users=db.relationship('User', backref='post')

    def __repr__(self):
        return f'<Post {self.id} {self.title} {self.created_at}>'

    # post_tag = db.relationship('tags', backref = 'post')
class Tag(db.Model):
    """Creates a tag for similar blogs"""

    __tablename__='tags'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.Text,
                    unique=True)

    def __repr__(self):
        return f'{self.name}'

    posts = db.relationship('Post', secondary='posttags', backref='tags')
class PostTag(db.Model):
    """Joins a post with a tag"""

    __tablename__='posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True,
                        nullable=False)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True,
                        nullable=False)

    

    def __rept__(self):
        return f'{self.tag_id}'    