from app import app
from flask import Flask, jsonify, request, Response, Blueprint
from app.database import models, db
from app.services import main_service

from datetime import datetime
import time
import threading

comment = Blueprint('comment', __name__)

@comment.route("/comment")
def get_comment_of_campaign():
    campaign_name = request.args.get('campaign')
    comments = main_service.get_comments_of_campaign(campaign_name)
    if not comments:
        return "No comments found", 404
    return jsonify(comments), 200