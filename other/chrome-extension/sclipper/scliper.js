CLIP_TYPE_TEXT="text";
CLIP_TYPE_LINK="link";
CLIP_TYPE_IMAGE="image";

SERVER_URL='https://swagclip.appspot.com/';

NULL = "null";

var oauth = ChromeExOAuth.initBackgroundPage({
  			'request_url': SERVER_URL+'_ah/OAuthGetRequestToken',
		  	'authorize_url': SERVER_URL+'_ah/OAuthAuthorizeToken',
  			'access_url': SERVER_URL+'_ah/OAuthGetAccessToken',
			'consumer_key': 'anonymous',
	  		'consumer_secret': 'anonymous',
			'scope': SERVER_URL,
			'app_name': 'SClip Chrome extension'
		});	


function contextOnClick(info, tab) {
        chrome.tabs.executeScript(null, {file: "contentscript.js"});        
	var clip = {
		"page" : NULL,
		"type" : NULL,
		"text" : NULL,
		"link" : NULL,
		"src"  : NULL
	};
	
	//Page URL
	if(info.pageUrl){
		clip["page"] = shortIt(info.pageUrl);
	}
	//Selection text
	if(info.selectionText){
		clip["text"] = shortIt(info.selectionText);
	}
	
	//Link text
	if(info.linkUrl){
		clip["link"] = shortIt(info.linkUrl);
	}	
	//Selected image
	if(info.srcUrl){
		clip["src"] = shortIt(info.srcUrl);
	}
	
	chrome.tabs.getSelected(null, function(tab) {
		chrome.tabs.sendRequest(tab.id, {clip:clip}, function(response) {
                        console.log("Action from page dialog : " + response.action);
                        //alert("sendSignedRequest - start" + response.action);
                        if(response.action!='cancel'){
                                                //Post clip to server
                                                oauth.authorize(function() {
                                                                        var url = SERVER_URL + "post/";
                                                                        var request = {
                                                                                                'method': 'GET',
                                                                                                'parameters': {
                                                                                                                        'page': clip["page"],
                                                                                                                        'text': clip["text"],
                                                                                                                        'link': clip["link"],
                                                                                                                        'src': clip["src"],
                                                                                                                        'comment' : shortIt(response.comment)
                                                                                                }                                                
                                                                        };
                                                                        console.log("Sending request to server : " + request);
                                                                        oauth.sendSignedRequest(url, published, request);
                                                                        console.log("Request sent.");
                                                });
                        }
  		});
	});
}

function shortIt(string){
                        if(string.length > 480) {
                                                string = string.substring(0,480)+"...";
                        }
                        return string.replace('\n',' ').replace('\t',' ');
}


function published(){}


function logout(){
	oauth.clearTokens();
}


var contexts = ["page","selection","link","image"];
chrome.contextMenus.create({"title": "Snip with swaglr", "contexts":contexts, "onclick": contextOnClick });
