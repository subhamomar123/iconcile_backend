from flask import Blueprint, request, jsonify
from models import DraftDetails, db

bp = Blueprint("draft_routes", __name__)


@bp.route("/draft/<int:hotel_id>", methods=["GET", "POST"])
def manage_draft(hotel_id):
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

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
