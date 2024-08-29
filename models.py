from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import uuid


db = SQLAlchemy()


class HotelDetails(db.Model):
    __tablename__ = "hotel_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    amenities = db.Column(db.Text)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    rating = db.Column(db.Numeric(3, 2))

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name="check_rating"),
    )


class ReservationsTracking(db.Model):
    __tablename__ = "reservations_tracking"
    hotel_id = db.Column(
        db.Integer, db.ForeignKey("hotel_details.id"), primary_key=True
    )
    visits_count = db.Column(db.Integer, default=0)
    bookings_count = db.Column(db.Integer, default=0)
    hotel = db.relationship(
        "HotelDetails", backref=db.backref("reservations_tracking", uselist=False)
    )


class DraftDetails(db.Model):
    __tablename__ = "draft_details"
    user_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(
        db.Integer, db.ForeignKey("hotel_details.id"), primary_key=True
    )
    draft = db.Column(db.Text)
    hotel = db.relationship("HotelDetails", backref=db.backref("draft_details"))


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class BookingDetails(db.Model):
    __tablename__ = "booking_details"

    booking_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel_details.id"), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Relationship to other tables (if needed)
    user = db.relationship("User", backref="bookings")
    hotel = db.relationship("HotelDetails", backref="bookings")

class UserVisitDetails(db.Model):
    __tablename__ = 'user_visit_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel_details.id'), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('visits', lazy=True))
    hotel = db.relationship('HotelDetails', backref=db.backref('user_visits', lazy=True))