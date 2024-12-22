from dotenv import load_dotenv
import os
import requests
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, session, jsonify
from celery import Celery
import shutil

# Load .env file if it exists
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Celery configuration
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

BOT_SECRET = os.getenv("BOT_SECRET")

# Ensure the variable is set
if not BOT_SECRET:
    raise ValueError("Missing required environment variable: BOT_SECRET")

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html', user=None)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

@app.route('/generate_token')
def generate_token():
    # Replace with your bot's secret and endpoint
    bot_secret = BOT_SECRET
    bot_endpoint = "https://directline.botframework.com/v3/directline/tokens/generate"

    headers = {
        "Authorization": f"Bearer {bot_secret}",
        "Content-Type": "application/json"
    }

    response = requests.post(bot_endpoint, headers=headers)
    if response.status_code == 200:
        token = response.json().get("token")
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Failed to generate token"}), 500

@app.route('/delete_album', methods=['POST'])
def delete_album():
    album_id = request.form.get('album_id')
    if album_id:
        delete_album_task.delay(album_id)
        return jsonify({"status": "Album deletion in progress"}), 202
    else:
        return jsonify({"error": "Album ID is required"}), 400

@celery.task
def delete_album_task(album_id):
    album_path = os.path.join('albums', album_id)
    if os.path.exists(album_path):
        shutil.rmtree(album_path)
        return {"status": "Album deleted successfully"}
    else:
        return {"error": "Album not found"}

if __name__ == '__main__':
    app.run(debug=True)
