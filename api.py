from flask import jsonify
from main import *
from model import *


@app.route("/api/influencer")
def api_influencer():
    influencers=Influencers.query.all()
    return  jsonify({ idx: {
        "influencer_id" : influencer.influencer_id,
    "user_id" : influencer.user_id,
    "img" :  "http://127.0.0.1:5000/image/"+str(influencer.influencer_id),
    "name" :  influencer.name,
    "category" : influencer.category,
    "niche" :  influencer.niche,
    "reach" :  influencer.reach} for idx, influencer in enumerate(influencers)}), 200


@app.route("/api/sponsor")
def api_sponsor():
    sponsors=Sponsors.query.all()
    return  jsonify({ idx: {
    "sponsor_id" : sponsor.sponsor_id,
    "user_id" : sponsor.user_id,
    "img" :  "http://127.0.0.1:5000/image1/"+str(sponsor.sponsor_id),
    "company_name" :  sponsor.company_name,
    "desc" : sponsor.desc,
    "industry" :  sponsor.industry} for idx, sponsor in enumerate(sponsors)}), 200


@app.route("/api/campaign")
def api_campaign():
    campaigns=Campaign.query.all()
    return  jsonify({ idx: {
        "sponsor_id" : campaign.sponsor_id,
    "user_id" : campaign.user_id,
    "brand_name" :  campaign.brand_name,
    "company_name" :  campaign.company_name,
    "desc" :  campaign.desc,
    "industry" :  campaign.industry,
    "start_date" :  campaign.start_date,
    "end_date" :  campaign.end_date,
    "budget" :  campaign.budget
    } for idx, campaign in enumerate(campaigns)}), 200


