

//Response action method
var response = null;

//Shows dialog window and returns back result.
chrome.extension.onRequest.addListener(
		function(request, sender, sendResponse) {
			sendResponse({title: $("title").html()});
		}
);


