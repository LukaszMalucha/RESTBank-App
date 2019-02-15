

(function ($) {
    "use strict";
    var mainApp = {

        initFunction: function () {
            /*MENU 
            ------------------------------------*/
            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });
       
	 
        },

        initialization: function () {
            mainApp.initFunction();

        }

    }
    // Initializing ///

}(jQuery));


/* ################################################################################### */

/* CHARITIES */
function deleteCharity(charity){
  var $charity = $(charity)
  $charity.parent().remove()
  var id = $charity.data('id')

  $.ajax({
    url: 'delete_charity/' + id,
    method: 'DELETE',
    beforeSend: function(xhr){
      xhr.setRequestHeader('X-CSRFToken', csrf_token)
    }
  })
}



function rejectCandidate(commitskill){
  var $commitskill = $(commitskill)
  $commitskill.parent().remove()
  var id = $commitskill.data('id')

  $.ajax({
    url: 'reject_candidate/' + id,
    method: 'DELETE',
    beforeSend: function(xhr){
      xhr.setRequestHeader('X-CSRFToken', csrf_token)
    }
  })
}















