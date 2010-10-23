/**
 * Provides interface to server functions.
 */
var sclipAPI = new SclipAPI();

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
		sclipAPI.deleteClip(id,onDeletedClip);
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