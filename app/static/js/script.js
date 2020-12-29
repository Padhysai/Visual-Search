console.log("Hello from app.js!");

function route(alttext){
    console.log(alttext)
    // var uri = window.origin + '/items'
    // fetch(uri, {
    //     method: "POST",
    //     body: JSON.stringify(alttext),
    //     cache: "no-cache",
    //     datatype:html,
    //     headers: new Headers({
    //       "content-type": "application/json"
    //     })
    //   })
    //   .then(function(response) {
    //     console.log(response)
    //   })
    //   .catch(function(error) {
    //     console.log("Fetch error: " + error);
    // });
    $.ajax({
      type:'POST',
      data:{'img':alttext},
      url:"/items",
      dataType: 'html',
      complete: function(){
        $("#loader").delay(500).fadeOut();
        console.log("OK");
      },
      success: function(response) {
        console.log(response);
        $('#nav_hide').hide();
        $('#fot_hide').hide();
        $(window).scrollTop(0);
        $('.results').html(response);
      }
    });
    
}