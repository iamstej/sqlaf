import sqlalchemy as db
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Booking(Base):

    __tablename__ = "booking"

    created_at = db.Column(db.DateTime)
    date = db.Column(db.Date)
    deposit = db.Column(db.Float)
    guest_names = db.Column(postgresql.ARRAY(db.String))
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    number_of_heads = db.Column(db.Integer)
    has_paid = db.Column(db.Boolean)
    time = db.Column(db.Time)
