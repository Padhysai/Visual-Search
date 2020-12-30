console.log("Hello from app.js!");


$(window).on('load', function () { 
  $(".loader").fadeOut(500);  
});




// -------------index.html--------------------//
$('#image').on('change',function(){
  //get the file name
  var fileName = $(this).val().split("fakepath")[1];
  fileValidation(fileName)
  //replace the "Choose a file" label
  $(this).next('.custom-file-label').html(fileName);
  $('#btn-indexsubmit').show();
})


function fileValidation(filePath) { 
  var allowedExtensions =  /(\.png|\.jpg|\.jpeg|\.PNG|\.JPG|\.JPEG)$/i; 
    
  if (!allowedExtensions.exec(filePath)) { 
      alert('Invalid file type'); 
      fileInput.value = ''; 
      return false; 
  }  
} 


// -------------index.html--------------------//

// -------------items.html--------------------//
function route(alttext){
  $(".loader").show(); 
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
        $(".loader").fadeOut(200);
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

// -------------items.html--------------------//