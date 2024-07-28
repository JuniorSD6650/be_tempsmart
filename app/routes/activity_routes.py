from flask import request, jsonify
from app.models import Activity, db

def init_activity_routes(app):
    @app.route('/activities', methods=['GET'])
    def get_activities():
        activities = Activity.query.all()
        return jsonify([activity.to_dict() for activity in activities])

    @app.route('/activities', methods=['POST'])
    def add_activity():
        data = request.get_json()
        new_activity = Activity(name=data['name'], description=data['description'])
        db.session.add(new_activity)
        db.session.commit()
        return jsonify(new_activity.to_dict()), 201
