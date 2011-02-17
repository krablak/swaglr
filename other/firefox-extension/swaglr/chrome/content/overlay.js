var Swaglr = {
    onLoad: function() {
        // initialization code
        this.initialized = true;
        this.strings = document.getElementById("Swaglr-strings");        
    },
    initSwag: function(e) {
        // Prepare swag model
        this.swag = {
          text: "null",
          page: "null",
          title: "null",
          src: "null",
          link: "null",
          type: "null"
        };
    },
    onMenuItemCommand: function(e) {
        log("*Swaglr quote action start.");
        //Prepare empty swag
        this.initSwag();
        //Get context element
        var element = document.popupNode;
        
        //Get page title
        this.swag.title = shortIt(document.title);
        //Get page URL
        this.swag.page = shortIt(window.top.getBrowser().selectedBrowser.contentWindow.location.href);
        
        //Check if context element is image
        var isImage = (element instanceof Components.interfaces.nsIImageLoadingContent && element.currentURI);
        if(isImage){
          this.swag.src = element.currentURI.prePath+element.currentURI.path;
          this.swag.type = "IMAGE";
        }
        
        // Set selected text to swag object
        var isText = document.commandDispatcher.focusedWindow.getSelection().toString() != "";
        if(isText && !isImage){
          this.swag.text = shortIt(document.commandDispatcher.focusedWindow.getSelection().toString());
          this.swag.type = "TEXT";
        }
        
        //Check if context element is link        
        var isLink = (element.nodeName == 'A');
        if(isLink && !isText && !isImage){
          this.swag.link = shortIt(element.getAttribute('href'));
          this.swag.type = "LINK";
        }        
        
        //In case that context element is not text or link or image ..swag will be page
        if(!isImage && !isLink && !isText){
          this.swag.type = "PAGE";
        }
        
        var win = window.openDialog("chrome://swaglr/content/post.xul","quoteOn", "chrome,centerscreen",this);
    },
    onToolbarButtonCommand: function(e) {
        // just reuse the function above.  you can change this, obviously!
        log("Call onToolbarButtonCommand - event : " + e);
    },
    getPostURL: function() {
      var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
      return prefs.getCharPref("extensions.Swaglr.post.url");
    }
    
    
    
};

function shortIt(string){
                        if(string.length > 480) {
                          string = string.substring(0,480)+"...";
                        }
                        return string.replace('\n',' ').replace('\t',' ');
              }

window.addEventListener("load", Swaglr.onLoad, false);

