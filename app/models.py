from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    sets = db.relationship('Sets', backref='sets', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

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


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    exercises = db.relationship('Exercise', backref='exercises', lazy='dynamic')

    def __repr__(self):
        return '%s' % self.name

    @property
    def serialize(self):
        return {
            'category_id': self.id,
            'name': self.name
        }


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    @property
    def serialize(self):
        return {
            'exercise_id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': str(Categories.query.get(self.category_id))
        }


class Sets(db.Model):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    repeats = db.relationship('Repeats', backref='repeats', lazy='dynamic')

    @property
    def serialize(self):
        repeats = list()
        sets = dict()
        r = Repeats.query.filter_by(set_id=self.id)
        exercise = Exercise.query.get(self.exercise_id)
        for repeat in r:
            repeats.append({'weight': repeat.weight, 'repeats': repeat.repeat, 'repeats_id': repeat.id})
        sets['exercise_name'] = exercise.name
        sets['exercise_id'] = exercise.id
        sets['category_id'] = exercise.category_id
        sets['category_name'] = str(Categories.query.get(exercise.category_id))
        sets['repeats'] = repeats
        return {
            'date': self.date.strftime("%Y-%m-%d"),
            'set_id': self.id,
            'items': sets
        }


class Repeats(db.Model):
    __tablename__ = 'repeats'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'))
    weight = db.Column(db.Float)
    repeat = db.Column(db.Integer)
