var Swaglr = {
    onLoad: function() {
        // initialization code
        this.initialized = true;
        this.strings = document.getElementById("Swaglr-strings");
    },
    onMenuItemCommand: function(e) {
        log("*Swaglr quote action start.");
        var element = document.popupNode;
        var isImage = (element instanceof Components.interfaces.nsIImageLoadingContent && element.currentURI);
        log("Is image : " + isImage);

        var wm = Components.classes["@mozilla.org/appshell/window-mediator;1"].getService(Components.interfaces.nsIWindowMediator);
        var mainWindow = wm.getMostRecentWindow("navigator:browser");
        log("text selection : " + document.commandDispatcher.focusedWindow.getSelection().toString());

        SERVER_URL='http://www.swaglr.com/';

        var oauth = ChromeExOAuth.initBackgroundPage({
            'request_url': SERVER_URL+'_ah/OAuthGetRequestToken',
            'authorize_url': SERVER_URL+'_ah/OAuthAuthorizeToken',
            'access_url': SERVER_URL+'_ah/OAuthGetAccessToken',
            'consumer_key': 'anonymous',
            'consumer_secret': 'anonymous',
            'scope': SERVER_URL,
            'app_name': 'Swaglr Chrome extension',
            'extension_name' : 'extensions.Swaglr'
        });
        oauth.authorize(function() {});
    },
    onToolbarButtonCommand: function(e) {
        // just reuse the function above.  you can change this, obviously!
        log("Call onToolbarButtonCommand - event : " + e);
    }
};

function finished(oauthObj) {
    alert(oauthObj);
}

window.addEventListener("load", Swaglr.onLoad, false);

