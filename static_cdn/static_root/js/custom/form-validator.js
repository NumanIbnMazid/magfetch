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
        $('#file-msg').html('');
        // $('#file-upload').val() = "";
    });
});

window.onload = function () {
    var file_to_upload = document.getElementById("file-upload");
    var doc_category_group = document.getElementById("doc-category-group");
    var img_category_group = document.getElementById("img-category-group");
    doc_category_group.style.display = "none";
    img_category_group.style.display = "none";
    file_to_upload.value = "";
}

function categoryFunction() {
    var file_to_upload = document.getElementById("file-upload");
    // file_to_upload.value == "";

    var img_ext = new Array();
    img_ext["jpg"] = 0;
    img_ext["JPG"] = 1;
    img_ext["jpeg"] = 2;
    img_ext["JPEG"] = 3;
    img_ext["png"] = 4;
    img_ext["PNG"] = 5;
    img_ext["svg"] = 6;
    img_ext["SVG"] = 7;

    var file_ext = new Array();
    file_ext["doc"] = 0;
    file_ext["DOC"] = 1;
    file_ext["docx"] = 2;
    file_ext["DOCX"] = 3;

    var doc_category = document.getElementById("doc-category");
    var doc_category_group = document.getElementById("doc-category-group");
    var img_category = document.getElementById("img-category");
    var img_category_group = document.getElementById("img-category-group");
    var msg_label = document.getElementById("file-msg");

    var loaded_file = file_to_upload.value;
    var loaded_file_ext = loaded_file.split('.').pop();

    // BASIC INITIALIZATION
    doc_category_group.style.display = "none";
    img_category_group.style.display = "none";
    doc_category.required = false;
    img_category.required = false;
    doc_category.setAttribute("name", "doc-category");
    img_category.setAttribute("name", "img-category");
    

    if (loaded_file_ext in file_ext) {
        doc_category.required = true;
        doc_category_group.style.display = "inline";
        doc_category.setAttribute("name", "category");
        // document.getElementById("message").innerHTML = "You selected: DOCUMENT";
    }
    else if (loaded_file_ext in img_ext) {
        img_category.required = true;
        img_category_group.style.display = "inline";
        img_category.setAttribute("name", "category");
        // document.getElementById("message").innerHTML = "You selected: IMAGE";
    }
    else{
        msg_label.innerHTML = "Your selected file is not valid to upload! Please upload valid Image or Document file.";
        msg_label.style.color = "red";
    }

    // var value = document.getElementById("doc-category").value;
    // document.getElementById("message").innerHTML = "You selected: " + loaded_file_ext;
}



$(document).ready(function () {
    $("#submit-button").click(function () {
        var file = $('#file-upload').val();
        if (file == '') {
            $('#messages').html('Please select a file!').css('color', '#B93232');
            $('#error-message').html('');
        }
    });
});
