CLIP_TYPE_TEXT="text";
CLIP_TYPE_LINK="link";
CLIP_TYPE_IMAGE="image";

SERVER_URL='http://www.swaglr.com/';

NULL = "null";

var oauth = ChromeExOAuth.initBackgroundPage({
  			'request_url': SERVER_URL+'_ah/OAuthGetRequestToken',
		  	'authorize_url': SERVER_URL+'_ah/OAuthAuthorizeToken',
  			'access_url': SERVER_URL+'_ah/OAuthGetAccessToken',
			'consumer_key': 'anonymous',
	  		'consumer_secret': 'anonymous',
			'scope': SERVER_URL,
			'app_name': 'Swaglr Chrome extension'
		});	


function contextOnClick(info, tab) {
    chrome.tabs.executeScript(null, {file: "contentscript.js"});        
	var clip = {
		"page" : NULL,
		"type" : NULL,
		"text" : NULL,
		"link" : NULL,
		"type" : NULL,
		"title" : NULL,
		"src"  : NULL
	};
	
	clip["page"] = shortIt(info.pageUrl);
	//Selection text
	if(info.selectionText){
		clip["text"] = shortIt(info.selectionText);
		clip["type"] = 'TEXT';
	}else
	//Selected image
	if(info.srcUrl){
			clip["src"] = shortIt(info.srcUrl);
			clip["type"] = 'IMAGE';
	}else	
	//Link url
	if(info.linkUrl){
		clip["link"] = shortIt(info.linkUrl);
		clip["type"] = 'LINK';
	}else
	//Page URL
	if(info.pageUrl){
		clip["type"] = 'PAGE';
	}
	
	chrome.tabs.getSelected(null, function(tab) {
		chrome.tabs.sendRequest(tab.id, {clip:clip}, function(response) {
                                    //Post clip to server
                                    oauth.authorize(function() {
                                                            var url = SERVER_URL + "api/clip/post/";
                                                            var request = {
                                                                                    'method': 'POST',
                                                                                    'parameters': {
                                                                                                            'page': clip["page"],
                                                                                                            'text': clip["text"],
                                                                                                            'link': clip["link"],
                                                                                                            'src': clip["src"],
                                                                                                            'type': clip["type"],
                                                                                                            'comment' : "null",
                                                                                                            'title' : shortIt(response.title)
                                                                                    }                                                
                                                            };
                                                            console.log("Sending request to server : " + request);
                                                           	oauth.sendSignedRequest(url, published, request);
                                                            var type_text = "What?!"
                                                            if(clip["type"]=="IMAGE"){
                                                            	type_text = "Image '" + clip["src"] + "'"
                                                            }else if(clip["type"]=="TEXT"){
                                                            	type_text = "Text selection '" + clip["text"] + "'"
                                                            }else if(clip["type"]=="LINK"){
                                                            	type_text = "Link '" + clip["link"] + "'"
                                                            }else if(clip["type"]=="PAGE"){
                                                            	type_text = "This page '" + shortIt(response.title) + "'"
                                                            }
                                                            var notification_text = type_text + ' was posted!';
                                                            //Show posted notification.
                                                            var post_not = webkitNotifications.createNotification(
                                                              '', 
                                                              'Posted!',
                                                              notification_text
                                                            );
                                                            post_not.show();
                                                            console.log(post_not);
                                                            console.log("Request sent.");
                                    });
  		});
	});
	
}

function shortIt(string){
                        if(string.length > 480) {
                                                string = string.substring(0,480)+"...";
                        }
                        return string.replace('\n',' ').replace('\t',' ');
}


function published(a,e){
	if(e.status!=200){
		// Show error notification.
        var error_not = webkitNotifications.createNotification(
          '', 
          'Sorry!',
          'Swag post failed! Please, try again later.'
        );
        error_not.show();
	}
}


function logout(){
	oauth.clearTokens();
}


var contexts = ["page","selection","link","image"];
chrome.contextMenus.create({"title": "Quote on swaglr", "contexts":contexts, "onclick": contextOnClick });
