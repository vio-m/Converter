$('#contactButton').click(function() {
    $('#alert').hide();
    $('#contact').fadeToggle('slow').delay(500).fadeToggle('slow');

});

$('#aboutButton').click(function() {
    $('#card-container, #about').slideToggle('slow', function() {
    });
});

















