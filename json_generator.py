# -*- coding:utf-8 -*-
__author__ = "Zachary Ma"
__date__ = "2017-01-13"

import json

file_html = open("wdj_cat.html")
file_json = open("category.json", "w")
file_cate = open("category.txt", "w")
cat_cnt = -1
sub_cnt = -1
jd = dict() # json dict
jd["name"] = "应用"
jd["children"] = list()

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
        big_cat["_children"].append(little_cat)
        file_cate.write("%02d%02d      %s\n" % (cat_cnt, sub_cnt, item))
    else:
        if big_cat is not None:
            jd["children"].append(big_cat)
        big_cat = dict()
        cat_cnt += 1
        sub_cnt = -1
        big_cat["name"] = "%s %02d" % (item, cat_cnt)
        big_cat["_children"] = list()
        file_cate.write("%02d      %s\n" % (cat_cnt, item))

file_json.write(json.dumps(jd,ensure_ascii=False,indent=2))
file_json.close()
