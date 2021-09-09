# Create your models here.

from app import db

from sqlalchemy import Column, Integer

class Example(db.Model):
    id = Column(Integer, primary_key=True)
