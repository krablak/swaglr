var DLG_ID = "com-ays-basic-modal-content ";
var DLG_PREV_ID = "com-ays-preview";

var DLG_POST_EVENT = "new function(){var postEvn = document.createEvent(\"Event\");postEvn.initEvent(\"postEvn\", true, true);window.dispatchEvent(postEvn);}"
var DLG_CANCEL_EVENT = "new function(){var cancelEvn = document.createEvent(\"Event\");cancelEvn.initEvent(\"cancelEvn\", true, true);window.dispatchEvent(cancelEvn);}"

var POST_HTML = "<div id=\""+DLG_ID+"\">\
<H3>Preview:</h3>\
<div id=\""+DLG_PREV_ID+"\"></div>\
<form method=\"post\" action=\"\" onsubmit=\"return:false\">\
<label for=\"comment\">Add comment to your clip:</label></br>\
<textarea class=\"com-ays-itextarea\" name=\"comment\" id=\"comment\"></textarea>\
</form>\
<p>\
<a class=\"com-ays-awesome\" id=\"btn_post\" onclick='"+DLG_POST_EVENT+"'>Post</a>\
<a class=\"com-ays-awesome\" id=\"btn_cancel\" onclick='"+DLG_CANCEL_EVENT+"'>Close</a></p>\
</div>";

//Response action method
var response = null;

//Shows dialog window and returns back result.
chrome.extension.onRequest.addListener(
		function(request, sender, sendResponse) {
                                response = sendResponse;
                                $(POST_HTML).modal();
                                prepareClipDetail(request.clip);
                                window.addEventListener('postEvn', onPost,false);
                                window.addEventListener('cancelEvn', onCancel,false);
		}
);

function onCancel(event){
                console.log("cancelEvent start -------------------------------------------------");
                console.log("Event for cancelation : "+event);                                                                
                callSendResponse({action: "cancel",comment: null});
                $.modal.close();
                removeListeners();
                console.log("cancelEvent end -------------------------------------------------");
}

function onPost(event){
                console.log("onPost start -------------------------------------------------");
                console.log("Event for comment post was launched : "+event);
                console.log("comment text area : " + $('#comment'));
                console.log($('#comment'));
                console.log($('#'+DLG_ID));                                                                
                var post_comment = $('#comment').val();
                console.log("Post comment text : " + post_comment);
                callSendResponse({action: "post",comment: post_comment});
                $.modal.close();
                removeListeners();
                console.log("onPost end -------------------------------------------------");    
}

function removeListeners(){
                window.removeEventListener ('postEvn', onPost, false);
                window.removeEventListener ('cancelEvn', onCancel, false);
}

//Prepares detail about selected clip content
function prepareClipDetail(clip){
                console.log(clip);
                var text = "";
                if(clip['src']!='null'){
                                console.log("Is Image Clip");
                                text = "<div class=\"com-ays-preview\"><img src=\""+clip['src']+"\"/></div>";
                }else if(clip['link']!='null'){
                                console.log("Is Link Clip");
                                text = "<div class=\"com-ays-preview\">"+clip['link']+"</div>";
                }else if(clip['text']!='null'){
                                text = "<div class=\"com-ays-preview\">"+clip['text']+"</div>";
                }else if(clip['page']!='null'){
                                console.log("Is Page Clip");
                                text = "<div class=\"com-ays-preview\">"+clip['page']+"</div>";
                }
                $('#'+DLG_PREV_ID).empty();
                $(text).appendTo('#'+DLG_PREV_ID);
}

function callSendResponse(params){
                if(response!=null){
                                console.log("Calling back the extension");
                                console.log(params);
                                response(params);
                }else{
                                 console.log("Response action is not set!");               
                }
}

