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
			url : "/clip-delete/"+id,
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
	
}