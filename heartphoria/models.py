from heartphoria import db


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    email = db.Column(db.TEXT, nullable=False, unique=True)
    name = db.Column(db.TEXT, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    role = db.Column(db.TEXT, nullable=False)
    dob = db.Column(db.DATE)
    gender = db.Column(db.TEXT)
    height = db.Column(db.INTEGER, default=0)
    weight = db.Column(db.INTEGER, default=0)
    fcode = db.Column(db.TEXT)

    reminder = db.relationship('Reminder', backref='user', lazy=True)
    appointment = db.relationship('Appointment', backref='user', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)


class Reminder(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.TIME, nullable=False)
    medication = db.Column(db.TEXT, nullable=False)
    quantity = db.Column(db.TEXT)


class Appointment(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    date_time = db.Column(db.TIMESTAMP, nullable=False)
    location = db.Column(db.TEXT, nullable=False)


class History(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DATE, nullable=False)
    description = db.Column(db.TEXT, nullable=False)


class Weather(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    last_update = db.Column(db.TIMESTAMP)
    weather_text = db.Column(db.TEXT)
    weather_icon = db.Column(db.INTEGER)
    temperature = db.Column(db.FLOAT)
    feel_temperature = db.Column(db.FLOAT)
    humidity = db.Column(db.INTEGER)
    wind_direction = db.Column(db.INTEGER)
    wind_direction_text = db.Column(db.TEXT)
    wind_speed = db.Column(db.FLOAT)
    uv_index = db.Column(db.INTEGER)
    uv_index_text = db.Column(db.TEXT)
    visibility = db.Column(db.FLOAT)
    cloud_cover = db.Column(db.INTEGER)
    pressure = db.Column(db.FLOAT)
    pressure_tendency = db.Column(db.TEXT)
    dew_point = db.Column(db.FLOAT)


class Hospital(db.Model):
    id = db.Column(db.TEXT, primary_key=True)
    last_update = db.Column(db.DATE)
    name = db.Column(db.TEXT)
    address = db.Column(db.TEXT)
    lat = db.Column(db.FLOAT)
    lng = db.Column(db.FLOAT)
