// Force To input Terms and Conditions
function checkForm(form) {
    if (!form.terms.checked) {
        $('#message').html('Please Read and Check Terms and Conditions').css('color', '#B93232')
            .css('background', '#FEF5C4').css('font-size', '15px');
        $('#submit').css('display', 'none');
        form.terms.focus();
        return false;
    }
    return true;
}

function clickCheck(e) {
    var agree = $('#agree').val();
    if (agree == 'check') {
        $('#message').html('')
        $('#submit').css('display', 'inline');
    } else {
        $('#message').html('Please Read and Check Terms and Conditions').css('color', '#B93232')
            .css('background', '#FEF5C4').css('font-size', '15px');
        $('#submit').css('display', 'none');
    }
}
// Clearing Error message on Click File Input
$(document).ready(function () {
    $("#file-upload").click(function () {
        $('#error-message').html('');
        $('#messages').html('').css('color', '#121538');
        $('#message').html('');
    });
});

$(document).ready(function () {
    $("#submit-button").click(function () {
        var file = $('#file-upload').val();
        if (file == '') {
            $('#messages').html('Please select a file!').css('color', '#B93232');
            $('#error-message').html('');
        }
    });
});