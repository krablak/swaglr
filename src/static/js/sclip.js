/**
 * Provides interface to server functions.
 */
var sclipAPI = new SclipAPI();

/****************************************Clip comment*****************************************************/
/**
 * ID of the currently edited clip.
 */
var EDITED_CLIP = null;

/**
 * Displays clip comment dialog.
 * @param id clip id for commenting.
 */
function showCommentDialog(id){
	if(EDITED_CLIP!=null){
		$('#clip-comment-edit-'+EDITED_CLIP).hide();
		$('#comment-textarea-'+EDITED_CLIP).html($('#clip-comment-edit-'+EDITED_CLIP).html());
		$('#clip-comment-view-'+EDITED_CLIP).fadeIn('fast');
	}
	EDITED_CLIP = id;
	var originalComment = $('#clip-comment-view-'+id).html();
	$('#comment-textarea-'+id).html(originalComment);
	$('#clip-comment-view-'+id).hide();
	$('#clip-comment-edit-'+id).fadeIn('fast');
	$('#comment-no-'+id).bind('click',{elid:id,origcomment:originalComment},function(event){
		$('#clip-comment-edit-'+event.data.elid).hide();
		$('#clip-comment-view-'+event.data.elid).html(event.data.origcomment);
		$('#comment-textarea-'+event.data.elid).html($('#clip-comment-edit-'+event.data.elid).html());
		$('#clip-comment-view-'+event.data.elid).fadeIn('fast');
	});
	$('#comment-yes-'+id).bind('click',{elid:id},function(event){
		var updatedComment = $('#comment-textarea-'+event.data.elid).val();
		sclipAPI.commentClip(event.data.elid,updatedComment,onCommentedClip,onCommentedError);
	});
}

/**
 * Function called after clip save. Stores updated text into clip comment area.
 */
function onCommentedClip(id,comment){
	$('#clip-comment-edit-'+id).hide();
	$('#clip-comment-view-'+id).html(comment);
	$('#comment-textarea-'+id).html(comment);
	$('#clip-comment-view-'+id).fadeIn('fast');
	EDITED_CLIP = null;
}

function onCommentedError(){
	alert('Sorry but clip commenting ends with unexpected error.');
	EDITED_CLIP = null;
}

/****************************************Clip delete*****************************************************/

/**
 * Displays clip delete dialog.
 * @param id clip id for deletetion.
 */
function showDeleteDialog(id){
	//Unbind old click events
	$('#delete-yes').unbind('click');
	$('#delete-no').unbind('click');
	//Bind function to delete dialog buttons
	$('#delete-yes').bind('click', function() {
		sclipAPI.deleteClip(id,onDeletedClip,onDeleteError);
		return false;
	});
	$('#delete-no').bind('click', function() {
		  $.modal.close();
		  return false;
	});
	//Open delete  dialog
	$("#delete-dialog").modal({
		onOpen: function (dialog) {
			dialog.overlay.fadeIn('fast', function () {
				dialog.data.show();
				dialog.container.fadeIn('fast');
			});
		},
		onClose: function (dialog) {
			dialog.data.fadeOut('fast', function () {
				dialog.container.fadeOut('fast', function () {
					dialog.overlay.fadeOut('fast', function () {
						$.modal.close();
					});
				});
			});
		}
	});
}

/**
 * Function called after clip deletion which removes the clip from page content.
 * 
 * @param id
 *            if of deleted clip.
 */
function onDeletedClip(id) {
	$.modal.close();
	$("#clip_box_"+id).fadeOut('slow', function() {
		$("#clip_box_"+id).remove();
	});
}

function onDeleteError(){
	$.modal.close();
	alert('Sorry but clip deleting ends with unexpected error.');
}

/**
 * Displays modal dialog for clicked clip.
 * 
 * @param clipId
 *            id of the clip.
 */
function showDetail(clipId) {
	$('#detail_' + clipId).modal({
		overlayClose : true
	});
}