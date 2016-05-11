from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)


class BodySize(db.Model):
    __tablename__ = 'bodysizes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    hip = db.Column(db.Float)
    arm = db.Column(db.Float)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime("%Y-%m-%d"),
            'chest': self.chest,
            'waist': self.waist,
            'hip': self.hip,
            'arm': self.arm,
            'weight': self.weight
        }
