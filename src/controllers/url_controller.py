from flask import Blueprint, jsonify, redirect, request

from data.models.url import Url
from exceptions.exception import URLException, URLShortnerError
from src.service.url_service import UrlService

url = Blueprint('url', __name__)

@url.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    if not data or 'original_url' not in data:
        return jsonify({"message": "No original url provided"}), 400

    original_url = data['original_url']
    try:
        service = UrlService()
        result = service.shorten_url(original_url)

        response = {
            'short_url': result['shortened_url'],
            'original_url': result['original_url'],
            'shortened_url': f'{request.url_root}{result["shortened_url"]}'
        }

        return jsonify(response), 201
    except URLException:
        return jsonify({"message": "URL shorten failed"}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500

@url.route('/<shortened_url>', methods=['GET'])
def redirect_shortened_url(shortened_url):
    try:
        print("Received short code:", shortened_url)
        url_service = UrlService()
        original_url = url_service.get_original_url(shortened_url)
        print("Look Up result: ", original_url)
        if not original_url:
            return jsonify({"message": "Original url not found"}), 404
        return redirect(original_url['original_url'])
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": "An error occurred"}), 500
