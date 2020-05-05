#---------------------------
#   Import Libraries
#---------------------------
import codecs
import os
import sys
import json
import math
import random as rd
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from PPSettings import PPSetting
from HugifyASettings import HugifyASettings

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Hugify Amplitude"
Website = "https://www.twitch.tv/wyllich"
Description = "Boosted"
Creator = "wyllich"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = HugifyASettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\hugifyasettings.json")
    ScriptSettings = HugifyASettings(SettingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if not data.IsChatMessage() or not data.IsFromTwitch():
        return
    
    if not ScriptSettings.Command in data.Message:
        return
   
    ppsetting = PPSetting()
    amp = 0
    PPSettingsFile = os.path.join(os.path.dirname(__file__), "Settings\ppsettings.json")
    with codecs.open(PPSettingsFile, encoding="utf-8-sig", mode="r") as f:
        ppsetting.__dict__ = json.load(f, encoding="utf-8")
        amp = ppsetting.Amplitude

    amplitudeCandidate = amp + float(data.GetParam(1))

    if amplitudeCandidate >= 30 and amplitudeCandidate <= 50:
        ppsetting.Amplitude = amplitudeCandidate
        with codecs.open(PPSettingsFile, encoding="utf-8-sig", mode="w+") as f:
            json.dump(ppsetting.__dict__, f, encoding="utf-8")
        with codecs.open(PPSettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
            f.write("var settings = {0};".format(json.dumps(ppsetting.__dict__, encoding='utf-8')))
        Parent.SendStreamMessage("OKIE DOKIE : New amplitude set to "+str(amplitudeCandidate))
    else:
        Parent.SendStreamMessage("I failed")

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
