/**
 * AJAX events filter.
 */
var SclipAPI = function() {
	
	/**
	 * Calls server to delete clip by id.
	 */
	this.deleteClip = function deleteClip(id,onSuccess) {
		$.ajax( {
			type : "GET",
			url : "/clip-delete/"+id,
			success : new function(){
				onSuccess(id);
			}
		});
	}
}