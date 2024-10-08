from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, value):
        if value is None or value.strip() == '':
            raise ValueError('requires each record to have a name')
        author = Author.query.filter(Author.name == value).first()
        if author is not None:
            raise ValueError('Name must be unique')
        return value
        
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must be exactly 10 digits long')
        return value

     

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError('Content must be less than 250 characters')
        
    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError('Summary must not exceed 250 characters')
    @validates('category')
    def validate_category(self, key, value):
        cat = ['Fiction', 'Non-Fiction']
        if value not in cat:
            raise ValueError('Category must be either Fiction or Non-Fiction')
    
    @validates('title')
    def validate_title(self, key, value):
        bait = ["Won't Believe" ,"Secret", "Top", "Guess"]
        if not any(word in value for word in bait):
            raise ValueError('Title must contain at least one of the bait words')


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
