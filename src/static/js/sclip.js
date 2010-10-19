/**
 * Initialize basic UC
 */
function initUI(){
}

/**
 * Displays modal dialog for clicked clip.
 * @param clipId id of the clip.
 */
function showDetail(clipId){
	$('#detail_'+clipId).modal({overlayClose:true});
}