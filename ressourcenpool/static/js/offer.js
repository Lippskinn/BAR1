// Created by Andreas Kirsch

$(document).ready(function() {

    if($("#id_mail").val() != "") {
        $("#contactForm input").prop("disabled", true);
        $("#editedContact").prop("checked", false);
    }

    $("#editedContact").change(function() {
        var checked = $(this).prop("checked");
        $("#contactForm input").prop("disabled", !checked);
    })

    $("#id_type").change(function() {

        let value = $(this).find(":selected").text();

        console.log("value=" + value);

        $("#Categories li:contains(" + value + ")").show();
        $("#Categories li:not(:contains(" + value + "))").prop("selected", false).hide();

    }).trigger("change");

    $("button").click(function () {
        $(this).preventDefault();
    })

    $('#confirm-delete').on('show.bs.modal', function(e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));

        $('.debug-url').html('Delete URL: <strong>' + $(this).find('.btn-ok').attr('href') + '</strong>');
    });
});


