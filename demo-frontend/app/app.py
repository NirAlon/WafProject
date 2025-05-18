import eventlet

eventlet.monkey_patch()

import os
from datetime import datetime

import requests
from flask import Flask, request, flash, url_for, render_template, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waf_logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

WAF_BASE = os.getenv("WAF_BASE", "http://localhost:8000")

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')

from flask_migrate import Migrate
migrate = Migrate(app, db)


def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'ip': ip,
                'city': data.get('city'),
                'country': data.get('country_name')
            }
    except:
        pass
    return {'ip': ip, 'city': None, 'country': None}


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    payload = db.Column(db.Text, nullable=False)
    allowed = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Float, nullable=True)
    ip = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.time,
            "type": self.type,
            "payload": self.payload,
            "allowed": self.allowed,
            "score": self.score,
            "ip": self.ip,
            "city": self.city,
            "country": self.country
        }


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        attack_type = request.form["attack_type"]
        payload = request.form["payload"]
        endpoint = f"{WAF_BASE}/{attack_type}_api"
        try:
            resp = requests.post(url=endpoint, json={"instance": [payload]}, timeout=5)
            data = resp.json()
            allowed = resp.status_code == 200 and data.get("allowed", False)
            score = data.get("score", None)
        except Exception as e:
            allowed, score, data = False, None, {"error": str(e)}

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        geo = get_ip_info(ip)

        entry = Log(
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type=attack_type,
            payload=payload,
            allowed=allowed,
            score=score,
            ip=geo['ip'],
            city=geo['city'],
            country=geo['country']
        )
        db.session.add(entry)
        db.session.commit()

        socketio.emit('new_log', {
            "id": entry.id,
            "time": entry.time,
            "type": entry.type,
            "payload": entry.payload,
            "allowed": entry.allowed,
            "score": entry.score,
            "ip": entry.ip,
            "city": entry.city,
            "country": entry.country
        })

        flash(f"{attack_type.upper()} test: {'ALLOWED' if allowed else 'BLOCKED'} (score = {score})",
              "success" if allowed else "danger")
        return redirect(url_for("index"))

    logs_db = Log.query.order_by(Log.id.desc()).all()
    logs = [entry.to_dict() for entry in logs_db]
    return render_template("index.html", logs=logs)


@app.route("/docs")
def docs():
    return render_template("docs.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=8003, debug=True)
