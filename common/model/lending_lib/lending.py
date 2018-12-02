from application import db

class Lending(db.Model):
    __tablename__ = 'lending'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    author = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    lending_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    shouldback_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    back_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    lending_amount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    lending_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    lending_college = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    lending_id = db.Column(db.String(13), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    book_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
