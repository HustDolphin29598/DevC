import crochet

crochet.setup()

from app import app
from flask import Flask, jsonify, request, Response, Blueprint
from app.database import models, db
from app.services import main_service
from app import app
from scrapy.crawler import CrawlerRunner
from datetime import datetime
import time
import threading
import json

campaign = Blueprint('campaign', __name__)
crawl_runner = CrawlerRunner()


@campaign.route("/campaign/create", methods=["POST"])
def create_campaign():
    data = request.get_json()
    name = data["name"]

    camp = models.Campaign.objects(name=name)

    if camp is not None and camp:
        return Response('Campaign existed !', status=500)

    description = data["description"]
    start_time = datetime.strptime(data["startTime"], '%Y-%m-%d').date()
    end_time = datetime.strptime(data["endTime"], '%Y-%m-%d').date()
    keyword = data["keyword"]
    links = data["links"]
    email = data["email"]
    password = data["password"]

    if email is None or not email or password is None or not password:
        return Response('Email or password not provided ! Campaign not be created yet !', status=500)

    campaign_obj = models.Campaign(
        name=name,
        description=description,
        startTime=start_time,
        endTime=end_time,
        keyword=keyword,
        links=links,
        status="working"  # to identify iéf it crawling and analysing data or done
    )

    try:
        campaign_obj.save()
    except Exception as ex:
        print(ex)
        return Response('Campaign can not be created !', status=500)

    # make sure campaign is saved to db
    time.sleep(1)

    campaign_thread = threading.Thread(target=main_service.create_campaign, kwargs={'model': app.model_lgr,
                                                                                    'campaign_name': name,
                                                                                    'email': email,
                                                                                    'password': password,
                                                                                    'keyword': keyword,
                                                                                    'links': links,
                                                                                    'start_time': start_time,
                                                                                    'end_time': end_time})
    campaign_thread.start()

    return Response('Campaign created !', status=201)


@campaign.route("/campaign", methods=["GET"])
def get_campaign_info():
    campaign_name = request.args.get('name')
    if campaign_name is None:
        return Response("Campaign not found !", status=404)
    campaign_obj = main_service.get_campaign(campaign_name)
    if campaign_obj is None:
        return Response("Campaign not found !", status=404)
    return jsonify(campaign_obj), 200


# @campaign.route("/crawl", methods=["POST"])
# def crawl():
#     data = request.get_json()
#     email = data['email']
#     password = data['password']
#     date = data['date']
#     links = data['links']
#     keyword = data['keyword']
#     campaign_name = data['campaign']
#     main_service.crawl(campaign_name, email, password, date, keyword, links)
#     return "ok", 200

#
# @campaign.route("/comment", methods=["GET"])
# def get_comment():
#     data = request.get_json()
#     campaign_name = data["campaign"]
#     posts = models.Post.objects(campaign=campaign_name)
#     texts = []
#     for post in posts:
#         comments = models.Comment.objects(post_id=post.post_id)
#         for comment in comments:
#             if comment is not None:
#                 texts.append(comment.text)
#
#     return jsonify(texts), 200


@campaign.route("/campaign/all", methods=["GET"])
def get_all_campaign():
    campaigns = main_service.get_all_campaign()
    if not campaigns:
        return Response("Campaign not found !", status=404)
    return jsonify(campaigns), 200
