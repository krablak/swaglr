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
				onSuccess(id);
			},
			error: function(xhr, ajaxOptions, thrownError){
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
				onSuccess(id,comment);
			},
			error: function(xhr, ajaxOptions, thrownError){
				onError();
			} 
		});
	}
	
	/**
	 * Calls server to comment clip by id.
	 */
	this.likeClip = function likeClip(id,onSuccess,onError) {
		$.ajax( {
			type : "POST",
			url : "/api/clip/like/",
			data: "id="+id,
			success : function(response){
				onSuccess(id);
			},
			error: function(xhr, ajaxOptions, thrownError){
				onError();
			} 
		});
	}
	
}