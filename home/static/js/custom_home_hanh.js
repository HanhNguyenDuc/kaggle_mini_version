$(document).ready(function() {
    // console.log($("#description_area").text());
    $(".description_area").each(function(index) {
        if ($(this).text().length > 200) {
            var text_content = $(this).text();
            $(this).html(text_content.substring(0, 200));
        }
    })
});