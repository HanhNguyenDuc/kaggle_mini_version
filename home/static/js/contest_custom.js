$(document).ready(function() {
    $('#content1').attr('style', 'display: inline-block; margin-left:20%; margin-right:20%;');
    $('#content2').attr('style', 'display: none;');
    $('#content3').attr('style', 'display: none;');
    $('#content444').attr('style', 'display: none;');
})

$('#tab1').click(function() {
    $('#content1').attr('style', 'display: inline-block;margin-left:20%; margin-right:20%;');
    $('#content2').attr('style', 'display: none;');
    $('#content3').attr('style', 'display: none;');
    $('#content444').attr('style', 'display: none;');
});

$('#tab2').click(function() {
    $('#content2').attr('style', 'display: inline-block;margin-left:20%; margin-right:20%;');
    $('#content1').attr('style', 'display: none;');
    $('#content3').attr('style', 'display: none;');
    $('#content444').attr('style', 'display: none;');
});


$('#tab3').click(function() {
    $('#content2').attr('style', 'display: none;');
    $('#content1').attr('style', 'display: none;');
    $('#content3').attr('style', 'display: inline-block; width:100%;');
    $('#content444').attr('style', 'display: none;');
})

$('#tab4').click(function() {
    $('#content2').attr('style', 'display: none;');
    $('#content1').attr('style', 'display: none;');
    $('#content444').attr('style', 'display: block; margin-left: 20%; margin-right: 20%');
    $('#content3').attr('style', 'display: none;');
})