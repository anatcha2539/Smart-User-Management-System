from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy

THAI_TZ = timezone(timedelta(hours=7))
def now_thai():
    return datetime.now(THAI_TZ)

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'          
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(120), nullable=False) 
    age = db.Column(db.Integer, nullable=False)  
    created_at = db.Column(db.DateTime, default=now_thai) 

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'created_at': self.created_at.isoformat()
        }