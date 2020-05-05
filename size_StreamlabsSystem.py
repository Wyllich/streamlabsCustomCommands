#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from MathsHelpers import generateRandomSizeInCm, convertFromCmToInch
from PPSettings import PPSetting

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Size"
Website = "https://www.twitch.tv/wyllich"
Description = "Sword fight? Kappa"
Creator = "wyllich"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = PPSetting()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global SettingsFile
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\ppsettings.json")
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    global ScriptSettings

    if not data.IsChatMessage() or not data.IsFromTwitch():
        return
    
    if not ScriptSettings.Command in data.Message:
        return
    
    #   PP Settings are read everytime a command is caught to allow parameters manipulation through hugifyM and hugifyA
    ScriptSettings = PPSetting(SettingsFile)

    sizeInCm = generateRandomSizeInCm(ScriptSettings.Amplitude, ScriptSettings.Minimum)
    sizeInInches = convertFromCmToInch(sizeInCm)

    chatMsg = "Hey "+data.User+"! Your PP size today is ... yuukeyEmilia ..."+str(sizeInCm)+" cm (or "+str(sizeInInches)+" inches) yuukeyEmilia"
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
