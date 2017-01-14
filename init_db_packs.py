# -*- coding:utf-8 -*-
__author__ = "Zachary Ma"
__date__ = "2017-01-14"


import json
import pymongo
import random

"""For cate_dict """

actually_run = raw_input("You actually want to run this?? (Y/N)\n This script will overwrite database.")
if actually_run != "Y":
    exit(11)

if __name__ == '__main__':
    client = pymongo.MongoClient(host="localhost", port=27017)
    db_appcat = client.get_database("appcat")
    cl_packs = db_appcat.get_collection("packs")
    cl_packs.drop()
    for i in range(47):
        if i == 46:
            cl_packs.insert_one({
                "pack_id": str(i).zfill(2),
                "author1": "",
                "author2": "",
                "author3": "",
                "start_app": str(i * 500),
                "end_app": str(23401)
            })
            break;
        cl_packs.insert_one({
            "pack_id": str(i).zfill(2),
            "author1": "",
            "author2": "",
            "author3": "",
            "start_app": str(i * 500),
            "end_app": str(i * 500 + 499)
        })