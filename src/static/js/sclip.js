/**
 * Provides interface to server functions.
 */
var sclipAPI = new SclipAPI();

/****************************************Clip comment*****************************************************/
/**
 * Displays clip comment dialog.
 * @param id clip id for commenting.
 */
function showCommentDialog(id){
	//Unbind old click events
	$('#comment-yes').unbind('click');
	$('#comment-no').unbind('click');
	//Set comment current value to edit field
	$('#comment-text').val($('#clip-comment-'+id).html());
	//Bind function to comment dialog buttons
	$('#comment-yes').bind('click', function() {
		var comment = $('#comment-text').val();
		sclipAPI.commentClip(id,comment,onCommentedClip,onDeleteError);
		return false;
	});
	$('#comment-no').bind('click', function() {
		  $.modal.close();
		  return false;
	});
	//Open comment  dialog
	$("#comment-dialog").modal({
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
 * Function called after clip save. Stores updated text into clip comment area.
 */
function onCommentedClip(id,comment){
	$.modal.close();
	$('#clip-comment-'+id).html(comment);
}

function onCommentedError(){
	$.modal.close();
	alert('Sorry but clip commenting ends with unexpected error.');
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