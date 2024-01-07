﻿import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from typing import Optional
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

#class for initial database structure (or schema) or means class for initial table
class User(db.Model, UserMixin):
    #if you want to change table name 
    #__tablename__ = "table_name_you_ want"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f'User: {self.username}'

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140), index=True, unique=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    
    author:so.Mapped[User] = so.relationship(back_populates='posts')
    
    def __repr__(self) -> str:
        return f'Post: {self.body}'