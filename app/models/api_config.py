from app.extensions import db
from flask import current_app


class APIConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(150))
    server = db.Column(db.String(150))
    token = db.Column(db.String(150))
    database = db.Column(db.String(150))
    os = db.Column(db.String(150))
    auth_method = db.Column(db.String(150))
    url_prefix = db.Column(db.String(150))

    def __repr__(self):
        return str({'id': self.id,
                'mode': self.mode,
                'server': self.server,
                'token': self.token,
                'database': self.database,
                'os': self.os,
                'url_prefix': self.url_prefix,
                'auth_method':self.auth_method
                })

class APITimer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(150))
    def __repr__(self):
        return f'<Timer "{self.time}">'

