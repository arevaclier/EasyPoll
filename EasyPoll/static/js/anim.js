/**
 * Created by Arthur on 09/01/2017.
 */
$(document).ready(function () {
    $('.progress-bar').each(function () {
        var value = $(this).attr("aria-valuenow");
        value = value.replace(/\s+/g, '');
        value += "%";
        $(this).css('width', value);
    })

    $('.title-date').each(function () {
        $(this).hide();
    });
});