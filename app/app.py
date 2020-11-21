from flask import Flask

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

app.run()
