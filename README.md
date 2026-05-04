# rasp-lib
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/primer-dad/rasp-lib)

`rasp-lib` is a lightweight Runtime Application Self-Protection (RASP) library for Flask applications. It provides a middleware to inspect incoming web requests for common security threats and block them in real-time.

## Features

-   **Flask Middleware:** Easy to integrate into any Flask application using a `@before_request` decorator.
-   **Threat Detection:** Identifies and blocks common web attack patterns:
    -   SQL Injection (SQLi)
    -   Cross-Site Scripting (XSS)
    -   Command Injection
    -   Path Traversal
-   **Real-time Blocking:** Malicious requests are blocked with a `403 Forbidden` response.
-   **JSON Logging:** Logs security incidents in a structured JSON format to the console and can be integrated with external logging services like Google Cloud Logging.

## Installation

You can install the library and its dependencies directly from the repository:

```bash
pip install git+https://github.com/primer-dad/rasp-lib.git
```

Dependencies:
-   `flask`
-   `google-cloud-logging`
-   `pytz`

## Usage

Integrate `rasp-lib` into your Flask application by using the `rasp_check_and_block` middleware.

### Basic Example

Here is a simple example of how to protect your Flask endpoints. The middleware will automatically inspect request arguments, form data, and JSON payloads.

```python
from flask import Flask, request, jsonify
from rasp_lib.middleware import rasp_check_and_block

app = Flask(__name__)

# Apply the RASP middleware to all incoming requests
@app.before_request
def check_request():
    return rasp_check_and_block()

@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.values.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == '__main__':
    app.run(debug=True)

```

Now, if a malicious request is sent, it will be blocked.

**Example Malicious Request:**
```bash
curl -X POST http://127.0.0.1:5000/ -d "name=<script>alert('xss')</script>"
```

**Blocked Response:**
```json
{
  "attack_type": "XSS",
  "matched_string": "<script>alert('xss')</script>",
  "message": "Blocked by RASP middleware",
  "status": "blocked"
}
```

### Logging with Google Cloud Logging

The middleware can integrate with a standard Python logger. This is useful for sending structured logs to services like Google Cloud Logging.

```python
import logging
import google.cloud.logging
from flask import Flask
from rasp_lib.middleware import rasp_check_and_block

# --- Boilerplate for Google Cloud Logging ---
# Note: Requires ADC authentication (e.g., `gcloud auth application-default login`)
client = google.cloud.logging.Client()
handler = google.cloud.logging.handlers.CloudLoggingHandler(client)
gcloud_logger = logging.getLogger('rasp-gcp-logger')
gcloud_logger.setLevel(logging.WARNING)
gcloud_logger.addHandler(handler)
# ---------------------------------------------

app = Flask(__name__)

@app.before_request
def check_request_with_logging():
    # Pass the logger to the middleware
    return rasp_check_and_block(logger=gcloud_logger)

@app.route("/")
def home():
    return "This is a protected endpoint."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

## Log Format

When a threat is detected, a JSON log is generated with the following structure. This is printed to the console and sent to the provided logger.

```json
{
    "message": "RASP: Security Incident Blocked",
    "attack_type": "SQL_INJECTION",
    "matched_pattern_snip": "union select",
    "source_input_key": "user_id",
    "request_uri": "/search",
    "request_method": "GET",
    "client_ip": "127.0.0.1",
    "input_value_snip": "1' union select 1,2,3 from users--"
}
