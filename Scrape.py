# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:39:01 2020
@author: austin
Scrape.py

"""

from bs4 import BeautifulSoup
import requests
import re


def main():
    heroname = input("Enter the hero name of the character you want to to get the stats for\n")
    herolevel = int(input("what level do you want to make this hero? "))
    
    hero = scrapeHeroData(heroname)
    hero = setStats(hero, herolevel)
    
    reportStats(hero)
    
    yesno = input("Would you like to write this information to a file? y/n?")
    if yesno == 'y' or yesno == 'Y':
        writeStats(hero)
        
    return


def writeStats(hero):
    
    f = open((hero.name + "report.txt"), "w" )
    f.write("Stats for hero: " + hero.name + " @ level: " + str(hero.trueLevel) + "\n")
    if (hero.primaryStat == 0):
        f.write("Primary Attribute: Strength\n")
    elif (hero.primaryStat == 1):
        f.write("Primary Attribute: Agility\n")
    elif (hero.primaryStat == 2):
        f.write("Primary Attribute: Intelligence\n\n")
        
    f.write("Current Strength: " + str(hero.trueStr) + "\n" )
    f.write("Current Agility: " + str(hero.trueAgi) + "\n")
    f.write("Current Intelligence: " + str(hero.trueInt) +"\n")
    f.write("Current HP: " + str(hero.trueHP) + "\n")
    f.write("Current HP regeneration: " + str(hero.trueHPregen)+ "\n" )
    f.write("Current MP: " + str(hero.trueManapool)+ "\n")
    f.write("Current MP regeneration: " + str(hero.trueMPRegen) + "\n")
    f.write("Current Armor: " + str(hero.trueArmor) + "\n")
    f.write("Current Damage Block: " + str(hero.damageBlock)+ "\n")
    f.write("Current Magic Resistance: " + str(hero.magicResist)+ "\n")
    f.write("Current Damage: " + str(hero.trueDamage)+ "\n")
    f.write("Current attacks per second: " + str(hero.trueAttacksPerSec)+ "\n")
    f.write("Damage per second: " + str((hero.trueDamage * hero.trueAttacksPerSec))+ "\n")
    f.write("Current Attack Speed: " + str(hero.trueAttackSpeed)+ "\n")
    f.write("Hero Base Attack Time: " + str(hero.baseAttackTime)+ "\n")
    f.close()
    print("file saved as: " + hero.name + "report.txt")
    
    
def reportStats(hero):
    
    print("Stats for hero: ", hero.name + " @ level: ", hero.trueLevel)
    print("")
    if (hero.primaryStat == 0):
        print("Primary Attribute: Strength")
    elif (hero.primaryStat == 1):
        print("Primary Attribute: Agility")
    elif (hero.primaryStat == 2):
        print("Primary Attribute: Intelligence")
        
    print("")
    print("Current Strength: " , hero.trueStr )
    print("Current Agility: " , hero.trueAgi )
    print("Current Intelligence: " , hero.trueInt )
    print("")
    print("Current HP: " , hero.trueHP)
    print("Current HP regeneration: " , hero.trueHPregen)
    print("Current MP: " , hero.trueManapool)
    print("Current MP regeneration: " , hero.trueMPRegen)
    print("")
    print("Current Armor: " , hero.trueArmor)
    print("Current Damage Block: " , hero.damageBlock)
    print("Current Magic Resistance: " , hero.magicResist)
    print("")
    print("Current Damage: " , hero.trueDamage)
    print("Current attacks per second: " , hero.trueAttacksPerSec)
    print("Damage per second: " , (hero.trueDamage * hero.trueAttacksPerSec))
    print("Current Attack Speed: " , hero.trueAttackSpeed)
    print("Hero Base Attack Time: " , hero.baseAttackTime)
    
    
    
def scrapeHeroData(heroName): 
    
    # grab website of chosen hero's page
    # the website used is https://dota2.gamepedia.com/Dota_2_Wiki on the landing page click any character avatar on this home page it will
    # give some corresponding url to the page we want to scrape. I think it's case sensitive
    
    website = "https://dota2.gamepedia.com/" + str(heroName)
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(website, headers)
    src = req.content
    soup = BeautifulSoup(src, 'html.parser' )
   
    ##################
    # Create a hero object
    character = Hero()
    ##################
    
    # grab the table of attributes it's the panel on the right of the page
    tablebox = soup.find(['table', 'class="infobox"'])
    string = tablebox.__str__() 
    
    # get the primary attribute
    character.primaryStat = getPrimary(string)
    
    # get hero name
    character.name = heroName
    
    # gets the 3 main attributes and their growth rates
    getAtributes(string, character)
    
    # gets everything else
    getOtherStats(string, character)    
    
    # return the hero object
    return character
    
def getOtherStats(string, character):
    
    # I'm just gonna sum up this whole function here, uses bunch of regular expressions to find a desired section of a page then
    # uses another regex to get the value from it then that value is assigned to the corresponding hero stat
    
    regex = (r"(<tr>\n"
	r"<th><a href=\"/Health\" title=\"Health\">Health</a>\n"
	r"</th>\n"
	r"<td>\d*\n"
	r"</td>)")
    
    match = re.findall(regex, string)
    regex = r"(\d.\d|\d+)"
    match = (re.findall(regex, str(match)))
    hp = int(match[0])
    character.baseHP = hp
    
    #regex = (r"(<th><a href=\"/Health_regeneration\" title=\"Health regeneration\">Health regen</a>\n"
	#r"</th>\n"
	#r"<td>\d+\n"
	#r"</td>)")
    
    regex = (r"(<th><a href=\"/Health_regeneration\" title=\"Health regeneration\">Health regen</a>\n"
	r"</th>\n"
	r"<td>(\d+|\d\.\d+)\n"
	r"</td)")
    
    match = re.findall(regex, string)
    regex = r"(\d+|\d\.\d+)"
    match = (re.findall(regex, str(match)))
    regen = float(match[0])
    character.baseRegen = regen    
    
    
    regex = (r"(<th><a href=\"/Mana\" title=\"Mana\">Mana</a>\n"
	r"</th>\n"
	r"<td>\d+\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+)"
    match = re.findall(regex, str(match))
    basemp = int(match[0])
    character.baseMP = basemp
    
    regex = (r"(<th><a href=\"/Mana_regeneration\" title=\"Mana regeneration\">Mana regen</a>\n"
	r"</th>\n"
	r"<td>(\d+|\d\.\d+)\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+|\d\.\d+)"
    match = (re.findall(regex, str(match)))
    mpregen = float(match[0])
    character.baseMPRegen = mpregen
    
    regex = (r"(<th><a href=\"/Armor\" title=\"Armor\">Armor</a>\n"
	r"</th>\n"
	r"<td>(\d+|-\d+)\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+|-\d+)"
    match = (re.findall(regex, str(match)))
    armor = int(match[0])
    character.baseArmor = armor
    
    regex = (r"(<th><a href=\"/Attack_damage\" title=\"Attack damage\">Damage</a>\n"
	r"</th>\n"
	r"<td>\d+‒\d+\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+)"
    match = (re.findall(regex, str(match)))
    baseDmg = (int(match[0]) + int(match[1])) / 2
    character.baseDamage = baseDmg
    
    regex = (r"(<a href=\"/Damage_block\" title=\"Damage block\">Damage block</a>\n"
	r"</th>\n"
	r"<td>\d\n"
	r"</td>)")
    
    match = re.findall(regex, string)
    regex = r"(\d+)"
    match = re.findall(regex, str(match))
    block = int(match[0])
    character.damageBlock = block
    
    regex = (r"(<a href=\"/Movement_speed\" title=\"Movement speed\">Movement speed</a></span>\n"
	r"</th>\n"
	r"<td>\d+\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+)"
    match = (re.findall(regex, str(match)))
    ms = int(match[0])
    character.movementSpeed = ms
    
    regex = (r"(<a href=\"/Attack_speed\" title=\"Attack speed\">Attack speed</a></span>\n"
	r"</th>\n"
	r"<td>\d+\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d+)"
    match = (re.findall(regex, str(match)))
    attackSpeed = int(match[0])
    character.attackSpeed = attackSpeed
    
    regex = (r"(<a class=\"mw-redirect\" href=\"/Base_attack_time\" title=\"Base attack time\">Base attack time</a>\n"
	r"</th>\n"
	r"<td>(\d|\d\.\d)\n"
	r"</td>)")
    match = re.findall(regex, string)
    regex = r"(\d.\d|\d)"
    match = re.findall(regex, str(match))
    bat = float(match[0])
    character.baseAttackTime = bat
    
def getAtributes(string, character):
    
    regex = (r"(<div><b>(\d+)</b>\s*\+\s*(\d|\d\.\d)</div>\n"
	r"<div><b>(\d+)</b>\s*\+\s*(\d|\d\.\d)</div>\n"
	r"<div><b>(\d+)</b>\s*\+\s*(\d|\d\.\d)</div>)")
    match = re.findall(regex, string)
    regex1 = r"(\d\.\d|\d+)"
    match = re.findall(regex1, str(match))
    
    character.strength = float(match[0])
    character.strengthGain = float(match[1])
    
    character.agility = float(match[2])
    character.agilityGain = float(match[3])
    
    character.intelligence = float(match[4])
    character.intelligenceGain = float(match[5])

def getPrimary(string):
    
    regex = r"(^.*)(<div id=\"primaryAttribute\">(\s*)<a href=\"/(\w*)\" title=\"(\w*)\">)(.*$)"
    match = re.findall(regex, string, re.MULTILINE)
    
    strength = r"(title=\"Strength\")"
    intel = r"(title=\"Intelligence\")"
    agi = r"(title=\"Agility\")"
    
    primary = -1
    if re.search(strength, str(match)):
        primary = 0
    if re.search(agi, str(match)):
        primary = 1
    if re.search(intel, str(match)):
        primary = 2
        
    return primary

def setStats(hero, level):
    # sets the big 3 attributes
    hero.trueLevel = level
    hero.trueStr = hero.strength + hero.strengthGain * hero.trueLevel
    hero.trueAgi = hero.agility + hero.agilityGain * hero.trueLevel
    hero.trueInt = hero.intelligence + hero.intelligenceGain * hero.trueLevel
    # computes attack speed from base AS and agility
    hero.trueAttackSpeed = hero.attackSpeed + hero.trueAgi
    hero.trueArmor = hero.baseArmor + hero.trueAgi * .17 # armor eq
        
    hero.trueHP = hero.baseHP + hero.trueStr * 20 # hp eq
    hero.trueHPregen = hero.baseRegen + hero.trueStr * .1
        
    hero.trueManapool = hero.baseMP + hero.trueInt * 12 #mp eq
    hero.trueMPRegen = hero.baseMPRegen + hero.trueInt * .05
        
    if (hero.primaryStat == 0):
        hero.trueDamage = hero.baseDamage + hero.trueStr
    elif (hero.primaryStat == 1):
        hero.trueDamage = hero.baseDamage + hero.trueAgi
    elif (hero.primaryStat == 2):
        hero.trueDamage = hero.baseDamage +  hero.trueInt
        
    hero.trueAttacksPerSec = hero.trueAttackSpeed *.01 / hero.baseAttackTime
    return hero
        
    
class Hero:
    baseHP = 0
    baseRegen = 0
    baseArmor = 0
    baseDamage = 0 
    damageBlock = 0
    baseMP = 0 
    baseMPRegen = 0
    magicResist = 0.25
    attackSpeed = 0
    
    strength = 0
    strengthGain = 0
    
    agility = 0
    agilityGain = 0
    
    intelligence = 0
    intelligenceGain = 0
    
    movementSpeed = 0
    primaryStat = -1
    name = "name"
    baseAttackTime = 0
    
    trueDamage = 0
    trueAttackSpeed = 0
    trueAttacksPerSec = 0
    trueArmor = 0
    trueHP = 0
    trueManapool = 0
    trueMPRegen = 0
    trueHPregen = 0
    trueLevel = 0
    trueStr = 0
    trueAgi = 0
    trueInt = 0
    
if __name__ =="__main__":
    main()
