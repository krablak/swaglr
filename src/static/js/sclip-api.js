/**
 * AJAX events filter.
 */
var SclipAPI = function() {
	
	/**
	 * Calls server to delete clip by id.
	 */
	this.deleteClip = function deleteClip(id,onSuccess,onError) {
		$.ajax( {
			type : "POST",
			url : "/api/clip/delete/",
			data: "id="+id,
			success : function(response){
				console.log("Clip delete call was successful.");
				onSuccess(id);
			},
			error: function(xhr, ajaxOptions, thrownError){
				console.log("Clip delete call fails with error.");
				console.log(xhr);
				onError();
			} 
		});
	}
	
	/**
	 * Calls server to comment clip by id.
	 */
	this.commentClip = function commentClip(id,comment,onSuccess,onError) {
		$.ajax( {
			type : "POST",
			url : "/api/clip/comment/",
			data: "id="+id+"&comment="+comment,
			success : function(response){
				console.log("Clip comment call was successful.");
				onSuccess(id,comment);
			},
			error: function(xhr, ajaxOptions, thrownError){
				console.log("Clip comment call fails with error.");
				console.log(xhr);
				onError();
			} 
		});
	}
	
}