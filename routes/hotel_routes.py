from flask import Blueprint, json, request, jsonify
from datetime import datetime
from models import (
    BookingDetails,
    UserVisitDetails,
    HotelDetails,
    ReservationsTracking,
    DraftDetails,
    db,
    User,
)

bp = Blueprint("hotel_routes", __name__)


@bp.route("/get_hotels", methods=["GET"])
def get_hotels():
    hotels = HotelDetails.query.all()
    hotel_list = []
    for hotel in hotels:
        hotel_list.append(
            {
                "id": hotel.id,
                "name": hotel.name,
                "amenities": hotel.amenities,
                "description": hotel.description,
                "location": hotel.location,
                "rating": hotel.rating,
                "visits_count": (
                    ReservationsTracking.query.filter_by(hotel_id=hotel.id)
                    .first()
                    .visits_count
                    if ReservationsTracking.query.filter_by(hotel_id=hotel.id).first()
                    else 0
                ),
            }
        )
    return jsonify(hotel_list), 200


@bp.route("/insert_hotels", methods=["POST"])
def insert_hotels():
    with open("hotels.json") as file:
        hotels = json.load(file)

    inserted_count = 0
    existing_count = 0

    for hotel in hotels:
        existing_hotel = HotelDetails.query.filter_by(
            name=hotel["name"], location=hotel["location"]
        ).first()

        if existing_hotel:
            existing_count += 1
        else:
            new_hotel = HotelDetails(
                name=hotel["name"],
                amenities=hotel["amenities"],
                description=hotel["description"],
                location=hotel["location"],
                rating=hotel["rating"],
            )
            db.session.add(new_hotel)
            inserted_count += 1

    db.session.commit()

    return jsonify(
        {
            "message": f"Hotels inserted successfully! {inserted_count} new entries added, {existing_count} entries already existed."
        }
    )


@bp.route("/hotel/<int:id>", methods=["GET"])
def get_hotel(id):
    hotel = HotelDetails.query.get(id)
    if not hotel:
        return jsonify({"message": "Hotel not found"}), 404

    tracking = ReservationsTracking.query.get(id)
    if not tracking:
        tracking = ReservationsTracking(hotel_id=id, visits_count=1, bookings_count=0)
        db.session.add(tracking)
    else:
        tracking.visits_count += 1

    user_id = request.args.get("user_id")
    user = db.session.query(User).filter_by(user_id=user_id).first()
    visit_data = {
        "hotel_id": id,
        "time": datetime.now().time(),
        "date": datetime.now().date(),
    }

    if user:
        visit_data["user_id"] = user.user_id

    now = datetime.now()
    new_visit = UserVisitDetails(**visit_data)
    db.session.add(new_visit)

    db.session.commit()

    return jsonify(
        {
            "id": hotel.id,
            "name": hotel.name,
            "amenities": hotel.amenities,
            "description": hotel.description,
            "location": hotel.location,
            "rating": hotel.rating,
            "visits_count": tracking.visits_count,
        }
    )


@bp.route("/hotel/checkout", methods=["POST"])
def checkout():
    data = request.json
    user_id = data.get("user_id")
    hotel_id = data.get("hotel_id")

    if not user_id or not hotel_id:
        return jsonify({"message": "user_id and hotel_id are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Invalid user_id"}), 404

    hotel = HotelDetails.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Invalid hotel_id"}), 404

    now = datetime.now()
    new_booking = BookingDetails(
        user_id=user_id, hotel_id=hotel_id, time=now.time(), date=now.date()
    )
    db.session.add(new_booking)

    reservation = ReservationsTracking.query.get(hotel_id)
    if reservation:
        reservation.bookings_count += 1
        reservation.visits_count += 1
    else:
        reservation = ReservationsTracking(hotel_id=hotel_id, bookings_count=1)

    db.session.add(reservation)
    db.session.commit()

    return (
        jsonify(
            {"message": "Checkout successful", "booking_id": new_booking.booking_id}
        ),
        201,
    )


@bp.route("/hotel/<int:hotel_id>/draft", methods=["GET", "POST"])
def manage_draft(hotel_id):
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

    hotel = HotelDetails.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Invalid hotel_id"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Invalid user_id"}), 404

    if request.method == "POST":
        data = request.json
        draft = data.get("draft")

        if not draft:
            return jsonify({"message": "draft is required"}), 400

        existing_draft = DraftDetails.query.get((user_id, hotel_id))
        if existing_draft:
            existing_draft.draft = draft
            message = "Draft updated successfully"
        else:
            new_draft = DraftDetails(user_id=user_id, hotel_id=hotel_id, draft=draft)
            db.session.add(new_draft)
            message = "Draft saved successfully"

        db.session.commit()

        return jsonify({"message": message}), 201

    elif request.method == "GET":
        draft_details = DraftDetails.query.get((user_id, hotel_id))
        if draft_details:
            return jsonify({"draft": draft_details.draft}), 200
        else:
            return jsonify({"message": "No draft found"}), 404


@bp.route("/hotel/bookings", methods=["GET"])
def get_hotel_bookings():
    hotel_id = request.args.get("hotel_id")

    if not hotel_id:
        return jsonify({"message": "hotel_id is required"}), 400

    hotel = HotelDetails.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Invalid hotel_id"}), 404

    reservations = ReservationsTracking.query.get(hotel_id)
    total_visits = reservations.visits_count if reservations else 0
    total_bookings = reservations.bookings_count if reservations else 0
    drafts = DraftDetails.query.filter_by(hotel_id=hotel_id).count()

    return (
        jsonify(
            {
                "total_visits": total_visits,
                "completed_bookings": total_bookings,
                "total_draft_bookings": drafts,
            }
        ),
        200,
    )


@bp.route("/suggest", methods=["GET"])
def suggest_hotels():
    user_id = request.args.get("user_id")

    if not user_id:
        top_hotels = (
            HotelDetails.query.order_by(HotelDetails.rating.desc()).limit(5).all()
        )
    else:
        last_visit = (
            UserVisitDetails.query.filter_by(user_id=user_id)
            .order_by(UserVisitDetails.date.desc(), UserVisitDetails.time.desc())
            .first()
        )

        if not last_visit:
            top_hotels = (
                HotelDetails.query.order_by(HotelDetails.rating.desc()).limit(5).all()
            )
        else:
            location = last_visit.hotel.location
            top_hotels = (
                HotelDetails.query.filter_by(location=location)
                .order_by(HotelDetails.rating.desc())
                .limit(5)
                .all()
            )

    hotels_data = [
        {
            "id": hotel.id,
            "name": hotel.name,
            "amenities": hotel.amenities,
            "description": hotel.description,
            "location": hotel.location,
            "rating": hotel.rating,
        }
        for hotel in top_hotels
    ]

    return jsonify(hotels_data)
