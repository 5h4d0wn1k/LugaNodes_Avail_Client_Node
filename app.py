from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# Base URL for the Avail Light Client API
BASE_URL = "https://api.lightclient.mainnet.avail.so"

# List of available endpoints
ENDPOINTS = [
    "/v1/latest_block",
    "/v1/confidence",
    "/v1/appdata",
    "/v1/operating_mode",
    "/v1/status",
    "/v2/latest_block",
    "/v2/status",
    "/v2/block_status",
    "/v2/block_header",
    "/v2/block_data",
    "/v2/submit_data"
]

# HTML template for the home page
HOME_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Avail Light Client API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        a { display: block; margin: 10px 0; color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Welcome to the Avail Light Client API!</h1>
    <p>Available endpoints:</p>
    {% for endpoint in endpoints %}
        <a href="{{ url_for('show_endpoint_result', path=endpoint.strip('/')) }}" target="_blank">{{ request.host_url }}api{{ endpoint }}</a>
    {% endfor %}
</body>
</html>
"""

# HTML template for displaying API results
RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>API Result</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }
        .error { color: red; }
        a { color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>{% if error %}Error{% else %}Result for Endpoint: {{ url }}{% endif %}</h1>
    <pre{% if error %} class="error"{% endif %}>{{ response }}</pre>
    <a href="{{ url_for('home') }}">Back to Home</a>
</body>
</html>
"""

@app.route('/api')
def home():
    return render_template_string(HOME_TEMPLATE, endpoints=ENDPOINTS)

def forward_request(url, method, params=None, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json(), False
    except requests.RequestException as e:
        return {"error": str(e)}, True

@app.route('/api/<path:path>', methods=['GET', 'POST'])
def dynamic_endpoint(path):
    url = f"{BASE_URL}/{path}"
    if request.method == 'GET':
        response_data, is_error = forward_request(url, 'GET', params=request.args)
    elif request.method == 'POST':
        response_data, is_error = forward_request(url, 'POST', data=request.json)
    return jsonify(response_data), 500 if is_error else 200

@app.route('/api/show/<path:path>', methods=['GET'])
def show_endpoint_result(path):
    url = f"{BASE_URL}/{path}"
    response_data, is_error = forward_request(url, 'GET', params=request.args)
    response_str = jsonify(response_data).data.decode('utf-8')
    return render_template_string(RESULT_TEMPLATE, url=url, response=response_str, error=is_error)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
