# -*- coding:utf-8 -*-
__author__ = "Zachary Mas"
file_html = open("wdj_cat.html")
file_cate = open("category.txt", "w")
cat_cnt = -1
sub_cnt = -1
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
        file_cate.write("%02d%02d      %s\n" % (cat_cnt, sub_cnt, item))
    else:
        cat_cnt += 1
        sub_cnt = -1
        file_cate.write("%02d      %s\n" % (cat_cnt, item))
