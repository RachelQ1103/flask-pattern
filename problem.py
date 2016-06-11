from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

import time
import shutil


db_path = 'problem.db'
app = Flask(__name__)
app.secret_key = 'asdjf1923'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String())
    timestamp = db.Column(db.DateTime(timezone=True), default=sql.func.now())

    def __init__(self, form):
        self.link = form.get('link', '')

    def __repr__(self):
        return u'<Problem {0} {1}>'.format(self.id, self.link)

    def save(self):
        db.session.add(self)
        db.session.commit()



def backup_db():
    backup_path = '{}.{}'.format(time.time(), db_path)
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    rebuild_db()
