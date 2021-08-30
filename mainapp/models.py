from .import db
import datetime

class Iperf(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    result = db.Column(db.String(1000))
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)