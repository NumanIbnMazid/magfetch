function send_query(check) {
    var values = [];
    for (i = 0; i < check.length; i++) {
        if (check[i].checked == true) {
            values.push(check[i].value);
        }
    }
    value_list = values.join();

    // console.log(values.join());

    var zip = new JSZip();
    var count = 0;
    var zipFilename = "zipFilename.zip";
    var urls = [
        values.join()
    ];
    
    $('#tst-msg').html(urls).css('color', '#B93232');

    urls.forEach(function (url) {
        var filename = "filename";
        // loading a file and add it in a zip file
        JSZipUtils.getBinaryContent(url, function (err, data) {
            if (err) {
                throw err; // or handle the error
            }
            zip.file(filename, data, {
                binary: true
            });
            count++;
            if (count == urls.length) {
                zip.generateAsync({
                    type: 'blob'
                }).then(function (content) {
                    saveAs(content, zipFilename);
                });
            }
        });
    });
}

