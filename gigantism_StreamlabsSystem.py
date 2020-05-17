#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import codecs
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from GigantismSettings import GigantismSettings

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Gigantism"
Website = "https://www.twitch.tv/wyllich"
Description = "Everyone likes it big and thicc"
Creator = "wyllich"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = GigantismSettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global SettingsFile
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\gigantismsettings.json")
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    global ScriptSettings

    if not data.IsChatMessage() or not data.IsFromTwitch():
        return
    
    if not data.GetParam(1) or not data.GetParam(2):
        return

    if not ScriptSettings.Command in data.Message:
        return

    if not Parent.HasPermission(data.User, ScriptSettings.Permission, ""):
        return
    
    ScriptSettings = GigantismSettings(SettingsFile)

    chatMsg = ""
    if data.GetParam(1) == "-a":
        if data.GetParam(2).lower() in ScriptSettings.Whitelist:
            chatMsg = "YOU ARE ALREADY BIG, YOU DUMB F*CK"
        else:
            ScriptSettings.Whitelist.append(data.GetParam(2).lower())
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(ScriptSettings.__dict__, f, encoding="utf-8")
            with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(ScriptSettings.__dict__, encoding='utf-8')))
            chatMsg = "YOU ARE BIG NOW PogU"

    if data.GetParam(1) == "-r":
        if not(data.GetParam(2).lower() in ScriptSettings.Whitelist):
            chatMsg = "ERROR 404"
        else:
            ScriptSettings.Whitelist.remove(data.GetParam(2).lower())
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(ScriptSettings.__dict__, f, encoding="utf-8")
            with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(ScriptSettings.__dict__, encoding='utf-8')))
            chatMsg = "Back to normality"
        
    Parent.SendStreamMessage(chatMsg)
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
