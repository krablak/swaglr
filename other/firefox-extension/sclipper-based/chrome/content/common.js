/**
*
* Provides simplified access to the swaglr extension preferences
*
**/
function getPref(key){
		 var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
         return prefs.getCharPref("extensions.Swaglr."+key);
}

function setPref(key,value){
		 var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
         return prefs.setCharPref("extensions.Swaglr."+key,value);
}

function hasPref(key){
		 var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
         return prefs.getCharPref("extensions.Swaglr."+key) != "";
}

/**
* Helper log function.
**/
function log(msg) {
  var consoleService = Components.classes["@mozilla.org/consoleservice;1"]
                                 .getService(Components.interfaces.nsIConsoleService);
  consoleService.logStringMessage(msg);
}