var googledocviewConstant = {
  OAUTH_PARAMS : {"oauth_version" : '1.0',
            "oauth_nonce":null,
                  "oauth_timestamp" : function() {return Math.floor(new Date().getTime() / 1000) ;}, 
                      "oauth_consumer_key" : 'anonymous',
                      "oauth_consumer_secret" : 'anonymous',
                      "oauth_callback" : "http://permurl.com/admin/googledocviewAddon.php", 
                      "oauth_signature_method" : "HMAC-SHA1",
                      "oauth_signature" : null
                      },
   NON_SIG_PARAMETERS : {"oauth_signature" : true},
   AUTHTYPE : {OAUTH:'oAuth', CLIENT_LOGIN : 'clientLogin' }
};

var googledocview = {
   getConfigPrefService : function (){
    return Components.classes['@mozilla.org/preferences-service;1']
                           .getService(Components.interfaces.nsIPrefService)
                           .getBranch('extensions.googledocview.options');
  },
  getCharPref: function(name, defaultValue){
    try{  
      return googledocview.getConfigPrefService().getCharPref("." + name);
    } catch(e){ }
    return defaultValue;
  }
}

var GDUtils = {
    getPrompt : function (){
      return Components.classes["@mozilla.org/embedcomp/prompt-service;1"]
                            .getService(Components.interfaces.nsIPromptService);
    },

    getOAuthParameterValue: function(paramName){
      var value = googledocview.getCharPref(paramName);
      if ( value )
        return value;
       value = googledocviewConstant.OAUTH_PARAMS[paramName];
      if ( typeof value == 'function')
        value = value.apply(null);
      return value;
    },
};


var googleConn = {
    oAuthTokens : { },
    oAuthScope : "http://www.swaglr.com/",
    getOAuthTokenUrl: '/_ah/OAuthGetRequestToken',
    OAuthLoginUrl:"http://www.swaglr.com/_ah/OAuthAuthorizeToken?oauth_token=",
    getOAuthAccessTokenUrl:"/_ah/OAuthGetAccessToken",
    getOAuthInfo : function(method, url, tokenSecret,customParams, optoutParams){
      var names = [];
      for (var name in googledocviewConstant.OAUTH_PARAMS )
        names.push(name);
      if ( !customParams)
        customParams = {};
      if ( !optoutParams)
        optoutParams = {};
        for(var name in customParams)
          names.push(name);       
      
        var accessor = { consumerSecret: GDUtils.getOAuthParameterValue('oauth_consumer_secret'),
                           tokenSecret   : tokenSecret};

        var message = { action: url,
                   method: method,
                   parameters: []
                          };        
      
      for(var i=0; i < names.length; i++){
        var name = names[i];
        if ( optoutParams[name])
          continue;
        var value = GDUtils.getOAuthParameterValue(name);
        if ( value == null || typeof value == "undefined" )
          value = customParams[name];
        if ( value == null || typeof value == "undefined" )
          continue;       
        message.parameters.push([name, value]);
      }
      
      OAuth.setTimestampAndNonce(message);
        OAuth.SignatureMethod.sign(message, accessor);

       // var parameterMap = OAuth.getParameterMap(message.parameters);
        message.authHeader = OAuth.getAuthorizationHeader("", message.parameters);
        
        message.baseString = OAuth.SignatureMethod.getBaseString(message);
      return message;
    },
    getAccessToken : function(){
      
      var message = googleConn.getOAuthInfo('POST',googleConn.googleUrl + googleConn.getOAuthAccessTokenUrl, 
          googleConn.oAuthTokens['oauth_token_secret'], { "oauth_verifier": googleConn.oAuthTokens['oauth_verifier'],
                "oauth_token":googleConn.oAuthTokens['oauth_token'],"scope":googleConn.oAuthScope});

        googleConn.httpReq = new XMLHttpRequest();
        googleConn.httpReq.open("POST", googleConn.googleUrl + googleConn.getOAuthAccessTokenUrl, false);
        googleConn.httpReq.setRequestHeader('User-Agent','Mozilla/5.0');
        googleConn.httpReq.setRequestHeader('GData-Version','3.0');
        googleConn.httpReq.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
        googleConn.httpReq.setRequestHeader('POST',googleConn.getOAuthAccessTokenUrl + '?scope=' + encodeURIComponent(googleConn.oAuthScope) +' HTTP/1.1');
        googleConn.httpReq.setRequestHeader('Authorization',message.authHeader);
        var params = "scope=" + encodeURIComponent(googleConn.oAuthScope);
        log("Params : " + params);        
        googleConn.httpReq.send(params);
        if (googleConn.httpReq.status == 200){
          googleConn.parseRequestToken(googleConn.httpReq.responseText);        
          googleConn.oAuthTokens['getAccessToken']=true;
          googleConn.authType = googledocview.getCharPref('authType', googledocviewConstant.AUTHTYPE.OAUTH);
          return true;
        }
           GDUtils.getPrompt().alert("Warning", "You choose to deny using this addon to access your data or  \n " +
                                                    "Connection to google account to verify your login failed . Connection status " + googleConn.httpReq.status);
        return false;    
    },
    
    parseRequestToken : function(responseText){
      
      var items = responseText.split('&');
      for(var i =0; i < items.length; i++){
         var namevalue = items[i].split('=');
          if ( namevalue.length == 2 ){
            googleConn.oAuthTokens[namevalue[0]]= decodeURIComponent(namevalue[1]);
          }
      } 
      
      
    },
};


//get oauth request token   
function oauthRequest() {
    googleConn.getAccessToken();
   };
