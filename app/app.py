from flask import Flask, render_template

from app.api.campaign_api import campaign
from app.api.comment_api import comment
from app.api.predict_api import predict
from app.api.post_api import post
from app.database import db
from app.services import main_service

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"db": "devc", "host": "localhost", "port": 27017}
app.register_blueprint(predict)
app.register_blueprint(campaign)
app.register_blueprint(comment)
app.register_blueprint(post)

db.initialize_db(app)
model = main_service.init_model()


@app.route("/")
def index():
    return render_template("campaign.html")


@app.route("/campaigns")
def campaigns():
    return render_template("campaign.html")


@app.route("/detail/comment")
def get_comment():
    return render_template("comment-campaign.html")


@app.route("/detail")
def get_campaign_detail():
    return render_template("detail-campaign.html")


@app.route("/create-campaign")
def create_campaign():
    return render_template("create-campaign.html")


@app.route("/login")
def login():
    return render_template("login.html")


app.run()
