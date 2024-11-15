# FastAPI server
from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

app = FastAPI()

client = MongoClient("localhost", 27017)
db = client["online_fine_tuning"]


# accept requests where the argument is a string corresponding to the object id of a message
@app.get("/feedback/{message_id}")
def feedback(message_id: str):
    # get the message from the database
    message = db["sent_emails"].find_one({"_id": ObjectId(message_id)})
    if message is None:
        return {"message": "Message not found"}

    # add the feedback field to the message
    message["click"] = datetime.now()

    # move the message to the feedback collection
    db["clicked"].insert_one(message)
    db["sent_emails"].delete_one({"_id": ObjectId(message_id)})

    return {"message": "Feedback added to message"}


def validity_check():
    # move all messages sent more than 14 days ago to the not_clicked collection
    not_clicked = db["sent_emails"].find(
        {"sent_at": {"$lt": datetime.now() - timedelta(days=14)}}
    )
    for message in not_clicked:
        db["not_clicked"].insert_one(message)
        db["sent_emails"].delete_one({"_id": message["_id"]})
    return {"message": "Validity check completed"}
