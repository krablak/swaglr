/**
 * Provides interface to server functions.
 */
var sclipAPI = new SclipAPI();

/****************************************Clip open*****************************************************/
var OPEN_CLIP = null;

function openClip(id){
	if(OPEN_CLIP==id){
		if(!$("#clip_box_"+OPEN_CLIP).hasClass("open")){
			OPEN_CLIP = null;			
		}
	}else{
		if(OPEN_CLIP!=null && OPEN_CLIP!=id){
			$("#clip_box_"+OPEN_CLIP).removeClass("open");
		}
		if(OPEN_CLIP!=id){
			$("#clip_box_"+id).addClass("open");
			$("#clip_box_"+id).unbind();
		}
		OPEN_CLIP=id;
	}
}

function closeClip(id){
	$("#clip_box_"+id).removeClass("open");
}

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
		cancelCommentEditor(EDITED_CLIP);
	}
	EDITED_CLIP = id;
	openCommentEditor(id);
	$('#comment-no-'+id).bind('click',{elid:id,origcomment:$('#clip-comment-view-'+id).html()},function(event){
		cancelCommentEditor(event.data.elid);
	});
	$('#comment-yes-'+id).bind('click',{elid:id},function(event){
		var updatedComment = $('#comment-textarea-'+event.data.elid).val();
		sclipAPI.commentClip(event.data.elid,updatedComment,onCommentedClip,onCommentedError);
	});
	return false;
}

function cancelCommentEditor(id){
	var originalComment = $('#clip-comment-view-'+id).html();
	$('#clip-comment-edit-'+id).hide();
	if(originalComment!="null" && originalComment!=""){
		$('#clip-comment-view-'+id).html(originalComment);
	}else{
		$('#clip-comment-view-'+id).html("");
		$('#clip-comment-view-div-'+id).hide();
	}
	$('#comment-textarea-'+id).html(originalComment);
	$('#clip-comment-view-'+id).fadeIn('fast');
	//Show edit buttons.
	showEditButtons(id,true);
}

function openCommentEditor(id){
	var originalComment = $('#clip-comment-view-'+id).html();
	if(originalComment!="null"){
		$('#comment-textarea-'+id).html(originalComment);
	}
	$('#clip-comment-view-div-'+id).show();
	$('#clip-comment-view-'+id).hide();
	$('#clip-comment-edit-'+id).fadeIn('fast');
	//Hide edit buttons.
	showEditButtons(id,false);
}

/**
 * Function called after clip save. Stores updated text into clip comment area.
 */
function onCommentedClip(id,comment){
	$('#clip-comment-edit-'+id).hide();
	$('#clip-comment-view-'+id).html(comment);
	$('#comment-textarea-'+id).html(comment);
	$('#clip-comment-view-'+id).fadeIn('fast');
	$('#edit-comment-btn-'+id).fadeIn('fast');
	var addBtn = $('#add-comment-btn-'+id);
	if(addBtn.length>0){
		addBtn.html("Edit comment");
	}
	showEditButtons(id,true);
	
	EDITED_CLIP = null;
}

/**
 * Shows or hide edit buttons for comment.
 * @param show true or false for showing or hiding edit buttons.
 */
function showEditButtons(id,show){
	var editBtn = $('#edit-comment-btn-'+id);
	var addBtn = $('#add-comment-btn-'+id);
	if(show){
		if(editBtn.length>0){
			editBtn.show();
		}else if(addBtn.length>0){
			addBtn.show();
		}
	}else{
		if(editBtn.length>0){
			editBtn.hide();
		}else if(addBtn.length>0){
			addBtn.hide();
		}
	}
}

/**
 * Called in case of problem during comment save.
 */
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