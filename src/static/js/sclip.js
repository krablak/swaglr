/**
 * Provides interface to server functions.
 */
var sclipAPI = new SclipAPI();
/**
 * **************************************Page init
 * actions****************************************************
 */
$(document).ready(initUI);

function initUI() {
	enableLikeButtons();
	enableFollowButtons();

}

/**
 * **************************************User follow
 * switch****************************************************
 */

function enableFollowButtons() {
	$('#follow-btn').click(
			function() {
				if ($(this) != null) {
					if ($(this).attr('follow') == "yes") {
						$(this).removeClass("blue");
						$(this).addClass("red");
						$(this).text("Unfollow");
						$(this).attr('follow', "no");
					} else {
						$(this).removeClass("red");
						$(this).addClass("blue");
						$(this).text("Follow");
						$(this).attr('follow', "yes");
					}
					sclipAPI.followSwitch($(this).attr('user'),
							onSwitchedFollow, onSwitchFollowError);
				}
				return false;
			});
}

function onSwitchedFollow(user) {
	var followBtn = $("#follow-btn-" + user);
}

function onSwitchFollowError(user) {
}

/**
 * **************************************Clip
 * like****************************************************
 */

/**
 * Get all like buttons and checks if they are enabled. For enabled buttons
 * displays them.
 */
function enableLikeButtons() {
	var likeBtns = $(".like-button");
	for ( var i = 0; i < likeBtns.length; i++) {
		var like_div = likeBtns[i];
		var like_div_id = like_div.getAttribute("id");
		if (like_div_id != null) {
			var clip_id = like_div_id.substring("like-button-div-".length,
					like_div_id.length);
			if ($.cookie("liked-clip-" + clip_id) == null) {
				$("#" + like_div_id).show();
			}
		}
	}
}

/**
 * Calls the like for given clip id on server.
 */
function like(id) {
	// Hide the like button
	$("#like-button-div-" + id).fadeOut('fast');
	incLikeNum(id);
	sclipAPI.likeClip(id, onLikedClip, onLikeError);
}

/**
 * Increments number of likes on clip element.
 */
function incLikeNum(id) {
	var like = parseInt($("#like-num-" + id).html());
	like++;
	$("#like-num-" + id).html(like)
}

/**
 * Called in case of successful like.
 */
function onLikedClip(id) {
	// Check if cookie for this like is already set
	var cookieId = "liked-clip-" + id;
	if ($.cookie(cookieId) == null) {
		$.cookie(cookieId, "liked", {
			expires : 7
		});
	}
}

/**
 * Called in case of failed like server call.
 */
function onLikeError() {
}

/**
 * **************************************Close Clip
 * detail****************************************************
 */
function closeClipDetail(id) {
	$("#page_detail_" + id).fadeOut('slow', function() {
		$("#page_detail_" + id).remove();
	});
	return false;
}

/**
 * **************************************Clip
 * open****************************************************
 */
var OPEN_CLIP = null;

function openClip(id) {
	if (OPEN_CLIP == id) {
		if (!$("#clip_box_" + OPEN_CLIP).hasClass("open")) {
			OPEN_CLIP = null;
		}
	} else {
		if (OPEN_CLIP != null && OPEN_CLIP != id) {
			$("#clip_box_" + OPEN_CLIP).removeClass("open");
		}
		if (OPEN_CLIP != id) {
			$("#clip_box_" + id).addClass("open");
			$("#clip_box_" + id).unbind();
		}
		OPEN_CLIP = id;
	}
}

function closeClip(id) {
	if (id != -1) {
		$("#clip_box_" + id).removeClass("open");
	} else if (OPEN_CLIP != null) {
		$("#clip_box_" + OPEN_CLIP).removeClass(OPEN_CLIP);
	}
}

/**
 * **************************************Clip
 * comment****************************************************
 */
/**
 * ID of the currently edited clip.
 */
var EDITED_CLIP = null;

/**
 * Displays clip comment dialog.
 * 
 * @param id
 *            clip id for commenting.
 */
function showCommentDialog(id) {
	if (EDITED_CLIP != null) {
		cancelCommentEditor(EDITED_CLIP);
	}
	EDITED_CLIP = id;
	openCommentEditor(id);
	$('#comment-no-' + id).bind('click', {
		elid : id,
		origcomment : $('#clip-comment-view-' + id).text()
	}, function(event) {
		cancelCommentEditor(event.data.elid);
	});
	$('#comment-yes-' + id).bind(
			'click',
			{
				elid : id
			},
			function(event) {
				var updatedComment = $('#comment-textarea-' + event.data.elid)
						.val();
				sclipAPI.commentClip(event.data.elid, updatedComment,
						onCommentedClip, onCommentedError);
			});
	return false;
}

function cancelCommentEditor(id) {
	var originalComment = $('#clip-comment-view-' + id).text();
	$('#clip-comment-edit-' + id).hide();
	if (jQuery.trim(originalComment) != "") {
		$('#clip-comment-view-' + id).html(originalComment);
	} else {
		$('#clip-comment-view-' + id).html("");
		$('#clip-comment-view-div-' + id).hide();
	}
	$('#comment-textarea-' + id).html(originalComment);
	$('#clip-comment-view-' + id).fadeIn('fast');
	// Show edit buttons.
	showEditButtons(id, true);
}

function openCommentEditor(id) {
	var originalComment = $('#clip-comment-view-' + id).text();
	if (jQuery.trim(originalComment)!="") {
		$('#comment-textarea-' + id).html(originalComment);
		$('#comment-textarea-' + id).val(originalComment);
	}else{
		$('#comment-textarea-' + id).html("");
		$('#comment-textarea-' + id).val("");
	}
	
	$('#clip-comment-view-div-' + id).show();
	$('#clip-comment-view-' + id).hide();
	$('#clip-comment-edit-' + id).fadeIn('fast');
	$('#comment-textarea-' + id).focus();
	
	// Hide edit buttons.
	showEditButtons(id, false);
}

/**
 * Function called after clip save. Stores updated text into clip comment area.
 */
function onCommentedClip(id, comment) {
	$('#clip-comment-edit-' + id).hide();
	$('#clip-comment-view-' + id).html(comment);
	$('#comment-textarea-' + id).html(comment);
	if (jQuery.trim(comment)!="") {
		$('#clip-comment-view-' + id).fadeIn('fast');
		$('#comment-ico-' + id).show();
		changeEditButtonText(id, "Edit comment");
	} else {
		$('#comment-nib-view-' + id).fadeOut('fast');
		$('#comment-ico-' + id).hide();
		changeEditButtonText(id, "Add comment");
	}
	$('#edit-comment-btn-' + id).fadeIn('fast');
	showEditButtons(id, true);

	EDITED_CLIP = null;
}

/**
 * Changes text on both edit buttons(edit-add)
 * 
 * @param id
 *            id of active clip
 * @param text
 *            text of comment button.
 */
function changeEditButtonText(id, text) {
	var addBtn = $('#add-comment-btn-' + id);
	if (addBtn.length > 0) {
		addBtn.html(text);
	}
	var editBtn = $('#edit-comment-btn-' + id);
	if (editBtn.length > 0) {
		editBtn.html(text);
	}
}

/**
 * Shows or hide edit buttons for comment.
 * 
 * @param show
 *            true or false for showing or hiding edit buttons.
 */
function showEditButtons(id, show) {
	var editBtn = $('#edit-comment-btn-' + id);
	var addBtn = $('#add-comment-btn-' + id);
	if (show) {
		if (editBtn.length > 0) {
			editBtn.show();
		} else if (addBtn.length > 0) {
			addBtn.show();
		}
	} else {
		if (editBtn.length > 0) {
			editBtn.hide();
		} else if (addBtn.length > 0) {
			addBtn.hide();
		}
	}
}

/**
 * Called in case of problem during comment save.
 */
function onCommentedError() {
	alert('Sorry but clip commenting ends with unexpected error.');
	EDITED_CLIP = null;
}

/**
 * **************************************Clip
 * delete****************************************************
 */

/**
 * Displays clip delete dialog.
 * 
 * @param id
 *            clip id for deletetion.
 */
function showDeleteDialog(id) {
	// Unbind old click events
	$('#delete-yes').unbind('click');
	$('#delete-no').unbind('click');
	// Bind function to delete dialog buttons
	$('#delete-yes').bind('click', function() {
		sclipAPI.deleteClip(id, onDeletedClip, onDeleteError);
		return false;
	});
	$('#delete-no').bind('click', function() {
		$.modal.close();
		return false;
	});
	// Open delete dialog
	$("#delete-dialog").modal({
		onOpen : function(dialog) {
			dialog.overlay.fadeIn('fast', function() {
				dialog.data.show();
				dialog.container.fadeIn('fast');
			});
		},
		onClose : function(dialog) {
			dialog.data.fadeOut('fast', function() {
				dialog.container.fadeOut('fast', function() {
					dialog.overlay.fadeOut('fast', function() {
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
	$("#clip_box_" + id).fadeOut('slow', function() {
		$("#clip_box_" + id).remove();
	});
	$("#page_detail_" + id).fadeOut('slow', function() {
		$("#page_detail_" + id).remove();
	});
}

function onDeleteError() {
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