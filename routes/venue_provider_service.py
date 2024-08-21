from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import *

venue_provider_service_bp = Blueprint('venue_provider_service_bp', __name__)

# Ensure the directory for file uploads exists
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@venue_provider_service_bp.route('/get/makeups', methods=['GET'])
@jwt_required()
def get_venue_providers():
    current_user = get_jwt_identity()
    try:
        venues = VenueProvider.find_all()
        return jsonify(venues), 200
    except Exception as e:
        return jsonify({"message": "Error in Fetching Venues", "error": str(e)}), 500

@venue_provider_service_bp.route('/postdata', methods=['POST'])
@jwt_required()
def create_venue_provider():
    current_user = get_jwt_identity()
    data = request.form
    files = request.files

    cover_picture = None
    picture_of_venue = None

    # Handle file uploads
    if 'coverPicture' in files:
        cover_picture = os.path.join(UPLOAD_FOLDER, secure_filename(files['coverPicture'].filename))
        files['coverPicture'].save(cover_picture)

    if 'pictureOfVenue' in files:
        picture_of_venue = os.path.join(UPLOAD_FOLDER, secure_filename(files['pictureOfVenue'].filename))
        files['pictureOfVenue'].save(picture_of_venue)

    # Create a VenueProvider instance
    venue_provider = VenueProvider(
        property=data.get('property'),
        name_of_place=data.get('nameOfPlace'),
        city=data.get('city'),
        state=data.get('state'),
        postal_code=int(data.get('postalCode')),
        address=data.get('address'),
        pin_location=int(data.get('pinLocation')),
        additional_service=data.get('additionalService'),
        price=float(data.get('price')),
        amenities=data.get('amenities'),
        place_description=data.get('placeDescription'),
        cover_picture=cover_picture,
        picture_of_venue=picture_of_venue
    )
    
    # Save the venue provider to the database
    result = venue_provider.save()
    
    if isinstance(result, Exception):
        return jsonify({"message": "Error in Creating Venue", "error": str(result)}), 500

    return jsonify({"message": "Successfully Created"}), 201

@venue_provider_service_bp.route('/<venue_id>', methods=['DELETE'])
@jwt_required()
def delete_venue_provider(venue_id):
    current_user = get_jwt_identity()
    try:
        result = mongo.db['VenueProvider'].delete_one({'_id': ObjectId(venue_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Venue not found"}), 404
        return jsonify({"message": "Venue deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting venue", "error": str(e)}), 500