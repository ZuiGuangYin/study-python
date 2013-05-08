#! /usr/bin/env python
#coding=utf-8
'''
Created on 2013-3-31
将info_fight_monster.xls转换为XML格式。转换分为以下几步：
step1： 读取xml文件，info_fight_monster.xls
step2： 解析出怪物基本信息，在base这个sheet里面，并放到一个xml文件中
step3： 解析出怪物的技能信息，并将技能信息插入到对应的xml中
step4：解析出怪物的奖励信息，并插入到对应XML中
step5：保存xml文件
@author: tylerzhu'''
from lxml import etree
import xlrd3, codecs
 
attrib = ["monsterSID", "classId", "type", "level", "attrib", #
          "attack", "skill", "define", "speed", "strength", #
          "luck", "name", "desc", "icon", "url", "frameRate"];
         
prize = ["monsterSID", "prizeSID", "type", "infoType", "gameID", "itemType",  #
         "itemSID", "num", "plusSID", "level", "name", "desc", "icon"];
        
skill = ["monsterSID", "skillSID", "skillLevel"];
 
info_fight_monster_xml = etree.ElementTree(etree.Element("data"));
 
def openxls():
    excel = xlrd3.open_workbook("xls/info_fight_monster.xls");
    base = excel.sheet_by_name("base");
    monster = excel.sheet_by_name("skill");
    prize = excel.sheet_by_name("prize");
    return (base, monster, prize);
 
def buildMonsterBase(xls):
    sheet = xls[0];
    for row in range(1, sheet.nrows):
        monsterAttr = {};
        for col in range(0, sheet.ncols):
            if sheet.cell(row, col).value != None and col < len(attrib):
                monsterAttr[attrib[col]] = sheet.cell(row, col).value;
                if type(monsterAttr[attrib[col]]) == float:
                    #print(str(round(monsterAttr[attrib[col]])))
                    monsterAttr[attrib[col]] = str(round(monsterAttr[attrib[col]]));
        sub = etree.SubElement(info_fight_monster_xml.getroot(), "monster", monsterAttr);
        sub.tail = "\n"
        #input()
 
def buildMonsterSkill(xls):
    sheet = xls[1];
    for row in range(1, sheet.nrows):
        skillAttr = {};
        for col in range(1, sheet.ncols):
            if sheet.cell(row, col).value != None and col < len(attrib):
                skillAttr[skill[col]] = sheet.cell(row, col).value;
                if type(skillAttr[skill[col]]) == float:
                    skillAttr[skill[col]] = str(round(skillAttr[skill[col]]));
        monsterSID = str(int(sheet.cell(row, 0).value));
        monster = info_fight_monster_xml.find("*[@monsterSID='" + monsterSID + "']");
        monster.text = ("\n\t");
        sub = etree.SubElement(monster, "skill", skillAttr);
        sub.tail = "\n\t"
 
def buildMonsterPrize(xls):
    sheet = xls[2];
    for row in range(1, sheet.nrows):
        prizeAttr = {};
        for col in range(1, sheet.ncols):
            if sheet.cell(row, col).value != None and col < len(attrib):
                prizeAttr[prize[col]] = sheet.cell(row, col).value;
                if type(prizeAttr[prize[col]]) == float:
                    prizeAttr[prize[col]] = str(round(prizeAttr[prize[col]]));
        monsterSID = str(int(sheet.cell(row, 0).value));
        monster = info_fight_monster_xml.find("*[@monsterSID='" + monsterSID + "']");
        monster.text = ("\n\t");
        sub = etree.SubElement(monster, "prize", prizeAttr);
        sub.tail = "\n\t"
 
def build():
    xls = openxls();
    buildMonsterBase(xls);
    buildMonsterSkill(xls);
    buildMonsterPrize(xls);
 
    #输出合并之后的配置
    ouput = codecs.open('output/info_fight_monster.xml', 'w', 'utf-8');
    ouput.write(etree.tounicode(info_fight_monster_xml.getroot()))
    ouput.close();
 
if  __name__ == '__main__':
    build();