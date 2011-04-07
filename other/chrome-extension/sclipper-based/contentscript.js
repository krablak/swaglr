

//Response action method
var response = null;

//Shows dialog window and returns back result.
chrome.extension.onRequest.addListener(
		function(request, sender, sendResponse) {
			var titleElement = $("title");
			var titleValue = "";
			if(titleElement.length>0){
				titleValue = titleElement.html();
			}
			sendResponse({title: titleValue});
		}
);


