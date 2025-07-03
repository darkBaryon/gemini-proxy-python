import os
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

@app.route('/', methods=['POST', 'OPTIONS'])
def gemini_proxy():
    if request.method == 'OPTIONS':
        return Response(status=204, headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        })

    if not API_KEY:
        return jsonify({"error": "API key is not configured on the server."}), 500

    incoming_data = request.json
    if not incoming_data:
        return jsonify({"error": "Request body must be JSON."}), 400

    params = {"key": API_KEY}
    try:
        response = requests.post(
            GEMINI_API_URL,
            params=params,
            json=incoming_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        return jsonify(response.json() if response.content else {"error": str(http_err)}), response.status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Request to Gemini API failed: {req_err}"}), 503

# 这个 health check 路由可以帮助 Vercel 确认服务是否启动
@app.route('/_health', methods=['GET'])
def health_check():
    return "OK", 200
