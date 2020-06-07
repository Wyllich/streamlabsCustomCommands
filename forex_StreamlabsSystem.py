#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import codecs
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from MathsHelpers import roundToSetDecimalPlace
from ForexSettings import ForexSettings


#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Foreign exchange"
Website = "https://www.twitch.tv/wyllich"
Description = "Everything comes at the right price"
Creator = "wyllich"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = ForexSettings()
global headers
headers = {'Authorization': 'Bearer FDF7u89fdC998875c8d7f'}

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global SettingsFile
    global ScriptSettings
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\forexsettings.json")
    ScriptSettings = ForexSettings(SettingsFile)

    return

def buildAPIQuoteQuery(baseCurrency):
    return "https://api.exchangeratesapi.io/latest?base="+baseCurrency

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    global ScriptSettings

    if not data.IsChatMessage() or not data.IsFromTwitch():
        return

    if not ScriptSettings.Command in data.Message:
        return

    if not Parent.HasPermission(data.User, ScriptSettings.Permission, ""):
        return

    if "cost" in data.Message.lower() and "does" in data.Message.lower():
        messageRegexResult = re.search("does (.*) of (.*) cost in ([a-zA-Z]{3})", data.Message)
        objectToBePriced = messageRegexResult.group(1)
        priceAndBaseCurrency = messageRegexResult.group(2)
        quoteCurrency = messageRegexResult.group(3).upper()

        priceAndBaseCurrencyRegexResult = re.search("(.*) ([a-zA-Z]{3})", priceAndBaseCurrency)
        priceBaseCurrency = priceAndBaseCurrencyRegexResult.group(1)
        baseCurrency = priceAndBaseCurrencyRegexResult.group(2).upper()

        quotesResult = Parent.GetRequest(buildAPIQuoteQuery(baseCurrency), headers)
        quotedict = json.loads(quotesResult)
    
        if quotedict["status"] != 200 :
            Parent.SendStreamMessage("Are you sure you want to search quotes from " + baseCurrency+ "?")
            return

        availableQuotes = json.loads(quotedict["response"])["rates"]
        date = json.loads(quotedict["response"])["date"]
        if not quoteCurrency in availableQuotes:
            Parent.SendStreamMessage("Sorry, there is no quote available from "+baseCurrency+" to "+quoteCurrency +" as of "+date)
            Parent.SendStreamMessage("Instead, here are your request of "+ objectToBePriced+ " in different currencies:")
            allQuotesMsg = ""
            for availQuoteCurrency in availableQuotes:
                priceQuoteCurrency = roundToSetDecimalPlace(availableQuotes[availQuoteCurrency]*float(priceBaseCurrency), 3)
                allQuotesMsg += str(priceQuoteCurrency)+ " "+availQuoteCurrency + "|"
            Parent.SendStreamMessage(allQuotesMsg)
        else:
            priceQuoteCurrency = roundToSetDecimalPlace(availableQuotes[quoteCurrency]*float(priceBaseCurrency),3)
            Parent.SendStreamMessage(objectToBePriced + " of " + priceBaseCurrency+" "+baseCurrency+" is worth " + str(priceQuoteCurrency)+" "+quoteCurrency+ " as of "+date)  

        return
    else:
        if not data.GetParam(1) or not data.GetParam(2) or not data.GetParam(3):
            return

        originalPrice = data.GetParam(1)
        baseCurrency = data.GetParam(2)
        quoteCurrency = data.GetParam(3)

        quotesResult = Parent.GetRequest(buildAPIQuoteQuery(baseCurrency), headers)
        quotedict = json.loads(quotesResult)
    
        if quotedict["status"] != 200 :
            Parent.SendStreamMessage("Are you sure you want to search quotes from " + baseCurrency+ "?")
            return
    
        availableQuotes = json.loads(quotedict["response"])["rates"]
        date = json.loads(quotedict["response"])["date"]
        if not quoteCurrency in availableQuotes:
            Parent.SendStreamMessage("Sorry, there is no quote available from "+baseCurrency+" to "+quoteCurrency)

        askedPrice = roundToSetDecimalPlace(availableQuotes[quoteCurrency]*float(originalPrice),3)
        Parent.SendStreamMessage(originalPrice+" "+baseCurrency+" is equal to " + str(askedPrice)+" "+quoteCurrency+", dated from "+date)
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
