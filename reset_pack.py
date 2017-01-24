# -*- coding:utf-8 -*-
# author zachary ma
# date 20170124

import sys
import pymongo

def reset(pack):
    if pack < 0 or pack >= 47:
        print("pack not in field.")
        return
    pack_zfill = str(pack).zfill(2)
    to_be_reset_list = list()
    for i in range(500):
        to_be_reset_list.append(str(pack * 500 + i))
    print("Connecting database")
    pydb = pymongo.MongoClient(host="yx.pkuos.org")
    appcat = pydb.get_database("appcat")
    apps = appcat.get_collection("apps")
    for app in to_be_reset_list:
        apps.update_one({"app_id":app}, {"$set":{"author2":"", "author1":"", "cate1":""}})
    pydb.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No enough arguments.")
        exit(1)
    to_be_reset = sys.argv[1]
    print("Pack %s is going to be reset." % to_be_reset)
    raw_input("Press enter key to continue...")
    reset(int(to_be_reset))
    print("Finished.")
