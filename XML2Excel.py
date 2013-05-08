#! /usr/bin/env python
#encoding=utf-8
'''
Created on 2013-5-6
将技能书info_fight_book。xml转换为excel格式。
例子只包含一个sheet，如果有多个sheet同样处理。
@author: tylerzhu
'''
from lxml import etree
import xlwt3 as xlwt
#写excel标题
#。。。
wb = xlwt.Workbook()
ws = wb.add_sheet("技能书")
 
tree = etree.parse('../xls/info_fight_book.xml')
root = tree.getroot()
row = 0
col = 0
for item in root:
    if len(item.attrib) == 0:
        continue
    row = row + 1
    col = 0
    for attr in item.attrib:
        ws.write(row, col, item.attrib[attr])
        col = col + 1
 
wb.save('../output/技能书.xls')