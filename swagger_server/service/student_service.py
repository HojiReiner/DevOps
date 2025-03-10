import os

from bson import ObjectId
from pymongo import MongoClient


if "MONGO_URI" in os.environ:
    client = MongoClient(os.environ['MONGO_URI'])
else:
    client = MongoClient('localhost', 27017)

db = client["app"]
student_collection = db["students"]
id_counter = db["id_counter"]

def add(student=None):
    results = student_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )

    if results:
        return 'already exists', 409

    student = student.to_dict()
    student.pop('_id')

    return str(student_collection.insert_one(student).inserted_id)


def get_by_id(student_id=None, subject=None):
    student_id = ObjectId(student_id)
    student = student_collection.find_one({"_id": student_id})

    if not student:
        return 'not found', 404

    student["_id"] = str(student.get("_id"))
    return student


def delete(student_id=None):
    student_id = ObjectId(student_id)
    student = student_collection.find_one({"_id": student_id})

    if not student:
        return 'not found', 404

    student_collection.delete_one({"_id": student_id})
    student["_id"] = str(student.get("_id"))
    return student
