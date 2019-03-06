$(document).ready(function () {
    $('#datatable').DataTable({
        "pagingType": "full_numbers",
        "scrollY": "50vh",
        "scrollX": true,
        "scrollCollapse": true,
        "paging": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "language": {
            "lengthMenu": "Show _MENU_ records per page",
            "zeroRecords": "Nothing found - sorry",
            "info": "Showing page _PAGE_ of _PAGES_",
            "infoEmpty": "No records available",
            "infoFiltered": "(filtered from _MAX_ total records)"
        }
    });
});