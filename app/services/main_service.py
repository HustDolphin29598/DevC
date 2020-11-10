from app.services.model_service import load_model_lgr, normalize_text, predict_lgr
from flask import jsonify
from app.database import models
import threading
import json
import logging
import time
import re
import os


def init_model():
    return load_model_lgr()


def predict_sentiment(model, text):
    text_en = normalize_text(text)
    return jsonify(text_en, predict_lgr(model, text_en))


def analyse_campaign(campaign_name):
    campaign = models.Campaign.objects(name=campaign_name).first()
    if campaign is None:
        logging.info("Campaign not found !")
        return

    total_comments = 0
    total_pos = 0
    total_neg = 0
    total_neu = 0

    posts = models.Post.objects(campaign=str(campaign_name))

    for post in posts:
        comments = models.Comment.objects(post_id=str(post.post_id))
        for comment in comments:
            if comment.text is None or not comment.text:
                comment.delete()
            total_comments += 1
            if comment.label == "positive":
                total_pos += 1
            elif comment.label == "negative":
                total_neg += 1
            elif comment.label == "neutral":
                total_neu += 1

    campaign.total_comments = total_comments
    campaign.total_pos = total_pos
    campaign.total_neg = total_neg
    campaign.total_neu = total_neu

    campaign.status = "done"
    campaign.save()


def crawl(campaign_name, email, password, keyword, start_time, end_time, links=[]):
    start_time_str = start_time.strftime("%Y-%m-%d")
    end_time_str = end_time.strftime("%Y-%m-%d")
    for link in links:
        print(link)
        sub = re.search(".com/(.*?)/", link)
        if sub:
            page = sub.group(1)
        else:
            return
        crawl_string = 'scrapy crawl fb -a email="' + email + '" -a password="' + password + '" -a campaign="' + campaign_name + '" -a starttime="' + start_time_str + '" -a endtime="' + end_time_str +'" -a keyword="' + keyword + '" -a page="' + page + '"'
        os.system("cd fbcrawler && " + crawl_string)


def get_campaign(name):
    campaign = models.Campaign.objects(name=name).first()
    return campaign


def get_comments_of_campaign(campaign_name):
    campaign = models.Campaign.objects(name=campaign_name).first()
    if campaign is None:
        return None
    posts = models.Post.objects(campaign=str(campaign.name))
    if posts is None:
        return None
    campaign_comments = []
    for post in posts:
        post_comments = []
        comments = models.Comment.objects(post_id=post.post_id)
        for comment in comments:
            # campaign_comments.append(comment)
            post_comments.append(comment.to_mongo())
        post.comments = post_comments
        campaign_comments.append(post)

    return campaign_comments


def predict_sentiment_campaign(model, campaign_name):
    posts = models.Post.objects(campaign=campaign_name)
    # if post is None:
    #     return None
    for post in posts:
        comments = models.Comment.objects(post_id=post.post_id)
        for comment in comments:
            if comment is not None:
                if comment.text is not None:
                    predict = predict_lgr(model, comment.text)
                    comment.label = predict[1]
                    comment.save()


def create_campaign(model, campaign_name, email, password, keyword, links, start_time, end_time):

    crawl(campaign_name, email, password, keyword, start_time, end_time, links)

    time.sleep(2)

    predict_sentiment_campaign(model, campaign_name)

    time.sleep(2)  # make sure everything is saved to database before analysing

    analyse_campaign(campaign_name)

def get_all_campaign():
    campaigns = models.Campaign.objects
    return campaigns