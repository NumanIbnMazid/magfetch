INFORMATION_TECHNOLOGY              = 0
COMPUTER_SCIENCE_ENGINEERING        = 1
ELECTRICAL_ELECTRONIC_ENGINEERING   = 2
MECHANICAL_ENGINEERING              = 3
APPLIED_PHYSICS                     = 4
APPLIED_CHEMESTRY                   = 5
ARCHITECTURE                        = 6
TEXTILE_ENGINEERING                 = 7

FACULTY_CHOICES                     = (
    (INFORMATION_TECHNOLOGY, 'INFORMATION TECHNOLOGY'),
    (COMPUTER_SCIENCE_ENGINEERING, 'COMPUTER SCIENCE & ENGINEERING'),
    (ELECTRICAL_ELECTRONIC_ENGINEERING, 'ELECTRICAL & ELECTRONIC ENGINEERING'),
    (MECHANICAL_ENGINEERING, 'MECHANICAL ENGINEERING'),
    (APPLIED_PHYSICS, 'APPLIED PHYSICS'),
    (APPLIED_CHEMESTRY, 'APPLIED CHEMESTRY'),
    (ARCHITECTURE, 'ARCHITECTURE'),
    (TEXTILE_ENGINEERING, 'TEXTILE ENGINEERING')
)



# File Category Scripts
// Starts Loading Category Based on file Load
        // var img_ext = ['jpg', 'jpeg', 'png', 'svg'];
        // var file_ext = ['doc', 'docx'];
        var doc_cat = document.getElementById('doc-category');
        var img_cat = document.getElementById('img-category');

        var img_ext = new Array();
        img_ext["jpg"] = 0;
        img_ext["jpeg"] = 1;
        img_ext["png"] = 2;
        img_ext["svg"] = 3;

        var file_ext = new Array();
        file_ext["doc"] = 0;
        file_ext["docx"] = 1;
        
        var loaded_file = $('#file-upload').val();
        var loaded_file_ext = loaded_file.split('.').pop();
        if (loaded_file_ext in file_ext)
        {
            doc_cat.required = true;
            $('#img-category-group').html('').css('display', 'none');
            doc_cat.setAttribute("name", "category");
            // var checker = "File Loaded";
        }
        else if (loaded_file_ext in img_ext)
        {
            img_cat.required = true;
            $('#doc-category-group').html('').css('display', 'none');
            img_cat.setAttribute("name", "category");
            // var checker = "Image Loaded";
        }
        else
        {
            $('#message').html('File is not valid!').css('color', '#B93232');
            // $('#submit-button').html('').css('display', 'none');
        }
        // $('#message').html(checker)
// Ends Loading Category Based on file Load