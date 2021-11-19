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