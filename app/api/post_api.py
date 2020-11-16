from app import app
from flask import Flask, jsonify, request, Response, Blueprint
from app.database import models

post = Blueprint('post', __name__)


@post.route("/post")
def get_posts_of_campaign():
    campaign_name = request.args.get('campaign')
    posts = models.Post.objects(campaign=campaign_name)
    if not posts:
        return "No posts found", 404
    return jsonify(posts), 200