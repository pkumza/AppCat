# -*- coding:utf-8 -*-
__author__ = "Zachary Ma"
__date__ = "2017-01-14"


import json
import random

"""For cate_dict """

actually_run = raw_input("You actually want to run this?? (Y/N)\n This script will overwrite database.")
if actually_run != "Y":
    exit(11)

file_html = open("wdj_cat.html")
cat_cnt = -1
sub_cnt = -1
jd = dict() # json dict
jd["name"] = "应用"
jd["children"] = list()

cate_dict = dict()
# 其他
cate_dict['\xe5\x85\xb6\xe5\xae\x83'] = "49"
# 全部游戏
cate_dict['\xe5\x85\xa8\xe9\x83\xa8\xe6\xb8\xb8\xe6\x88\x8f'] = "99"
# 旅游
cate_dict['\xe6\x97\x85\xe6\xb8\xb8'] = "05"


big_cat = None
for line in file_html:
    if "<p>app_game_gap_reserve</p>" in line:
        cat_cnt += 1
        continue
    if line.find("</a>") == -1:
        continue
    ll = line[:line.find("</a>")]
    item = ll[ll.rfind(">") + 1:]
    if "child-cate" in line:
        sub_cnt += 1
        little_cat = dict()
        little_cat["name"] = "%02d%02d %s" % (cat_cnt, sub_cnt, item)
        cate_dict[item] = "%02d%02d" % (cat_cnt, sub_cnt)
        big_cat["_children"].append(little_cat)

    else:
        if big_cat is not None:
            jd["children"].append(big_cat)
        big_cat = dict()
        cat_cnt += 1
        sub_cnt = -1
        big_cat["name"] = "%s %02d" % (item, cat_cnt)
        cate_dict[item] = "%02d" % (cat_cnt)
        big_cat["_children"] = list()

"""Main"""

import pymongo
import glob
import os.path

if __name__ == '__main__':
    """
    敏捷开发，所以我就不顾及太多规定了

    内容: 扫描data文件夹，然后分为很多个pack，然后入库。
    """
    files = glob.glob("/Users/marchon/Projects/WdjData/*")
    client = pymongo.MongoClient(host="localhost", port=27017)
    db_appcat = client.get_database("appcat")
    cl_apps = db_appcat.get_collection("apps")
    cl_apps.drop()
    cnt = 0
    for long_file_name in sorted(files):
        file_type = long_file_name[long_file_name.rfind("."):]
        if file_type == ".png":
            continue
        if file_type != ".txt":
            print("有妖气")
            raise AssertionError
        file_name = os.path.basename(long_file_name)
        categories = file_name[1:file_name.find("]")]
        cate_id_list = list()
        for category in categories.split(";"):
            cate_id_list.append(cate_dict[category])
        package_name = file_name[file_name.find("]") + 1:file_name.rfind(".")]
        png_file_name = file_name[:-4] + ".png"
        description_file = open(long_file_name, "r")
        descriptions = description_file.readlines()
        app_description = ""
        app_name = ""
        tags = ""
        for line_cnt in range(len(descriptions)):
            if descriptions[line_cnt] == "Name\n":
                app_name = descriptions[line_cnt + 1][:-1].strip()
            if descriptions[line_cnt] == "Tag\n":
                tags = descriptions[line_cnt + 1][:-1]
            if descriptions[line_cnt] == "Description\n":
                app_description = "".join(descriptions[line_cnt+1:])

        cl_apps.insert_one({
            "app_id": str(cnt),
            "package_name": package_name,
            "official_categories": ";".join(cate_id_list),
            "png": png_file_name,
            "app_name": app_name,
            "tags": tags,
            "description": app_description,
            "author1" : "",
            "author2" : "",
            "author3" : "",
            "cate1": "",
            "cate2": "",
            "cate3": ""
        })
        cnt += 1


    """
    mc = pymongo.MongoClient(host="localhost", port=27017)
    t = mc.get_database(name="test")
    a = t.get_collection(name="c")
    a.insert_one({"test":"haha"})
    """