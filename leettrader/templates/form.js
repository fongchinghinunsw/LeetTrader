$(document).ready(function() {
  $('form').on('submit', function(event) {
    $.ajax({
      data: {
        email: $('#email-input').val()
      },
      type: 'POST',
      url: '/process'
    })
    .done(function() {
      $("#button-reset").val="fuckme";
    });


    event.preventDefault()
  });

});