/* UI */


function blur(elemID) {
  $('#' + elemID).css('filter', 'blur(5px)');
}

function unblur(elemID) {
  $('#' + elemID).css('filter', 'blur(0px)');
}

function blurAll() {
  blur('chart-area');
  blur('schedule-list');
  blur('status');
  blur('variable-list');
  blur('unsaved-secret-list');
  blur('saved-secret-list');
  blur('deploy-steps');    
}

function hideModal(modalID) {
  $('#' + modalID).modal('hide');
}

function showModal(modalID) {
  $('#' + modalID).modal({
    backdrop: 'static',
    keyboard: false
  });
  $('#' + modalID).modal('show');     
}

var confetti;
function shootConfetti(targetID, params) {
    // https://github.com/loonywizard/js-confetti
    confetti = new JSConfetti($('#message-modal'));
    confetti.addConfetti(params).then(() => function(){confetti.clearCanvas()});
    return confetti;
}

function showThemedModal(modalID, theme, headline=null, body=null) {
    if (theme === 'celebration') {
        shootConfetti(modalID, {
            emojis: ['🌈', '⚡️', '🦄', '✨', '💫', '🌸'],
            confettiRadius: 3,
            confettiNumber: 100,
        });
    } else if (theme === 'clap') {
        shootConfetti(modalID, {
            // emojis: ['👏'],
            confettiRadius: 10,
            confettiNumber: 200,
        });
    }
    if (headline) {
        $('#' + modalID + '-header-text').text(headline);
    }
    if (body) {
        $('#' + modalID + '-body-content').html(body);
    }
    showModal(modalID);
}

function showMessageModal(theme, headline, body, buttonLabel) {
    $('#message-modal-button-label').html(buttonLabel);
    showThemedModal('message-modal', theme, headline, body);
}

function showLinkedInModal() {
    showThemedModal('linkedin-modal', 'clap', null, null);
}

function showAlert(alertText, style='danger', elemID='alert', dismissable=true, disappear_seconds=10) {
    css = 'style="-webkit-animation: cssAnimation 5s forwards; animation: cssAnimation 5s forwards;"'
    css ='';
    if (dismissable) {
        $('#' + elemID)[0].innerHTML = '<div role="alert" class="alert alert-' + style + ' alert-dismissible" ' + css +'><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><span id="alert-text">' + alertText + '</span></div>';    
    } else {
        $('#' + elemID)[0].innerHTML = '<div class="alert alert-' + style + '" role="alert" ' + css + '><span>' + alertText + '</span></div>';
    }
}

function setProgressBar(target, percent, showPercent=true, text='') {
    target.show();
    var percentBar = target.children();
    percentBar.attr('style', 'width: '+ percent.toString() + '%;');
    percentBar.attr('aria-valuenow', percent);
    if (showPercent) {
        text += Math.round(percent) + '%'
    }
    percentBar.html(text);
}

function updateProgressBar(e) {
    var percent = 100.0 * e.loaded / e.total;
    setProgressBar($('#progress-bar'), percent);
}

function resetMediaUI() {
    $('#import-media-button').prop('disabled', false);    
    $('#progress-bar').hide();
    $('#remove-media').hide();
    $('#progress-bar-progress').css('width: 0%;')
}

function updatePostSubmitButton() {
    var postTs = _st.get('postTimestamp');
    var contentUid = _st.get('ContentUid');
    if (postTs != null) {
        $('#unschedule-icon').show();
        $('#save-as-draft-icon').hide();
        $('#save-button').prop('disabled', false);
        if (!contentUid) {
            $('#submit-post-button').html('Schedule');
        } else {
            $('#submit-post-button').html('Update');
        }
    } else {
        $('#unschedule-icon').hide();
        $('#save-as-draft-icon').show();        
        $('#submit-post-button').html('Post now'); 
    }    
}

function resetMediaUploadUI() {
    $('#import-media-button').prop('disabled', false);
    $('#progress-bar').hide();
    $('#progress-bar-progress').css('width: 0%;');
}

function clearPostSearchField() {
    $('#searchField').val('');
    postTable.lookUp('');
}