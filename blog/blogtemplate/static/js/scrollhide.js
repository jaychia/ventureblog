jQuery(document).ready(function($){
	console.log('here');
});

$(function(){
	console.log('running');
	var didScroll;
	var lastScrollTop = 0;
	var delta = 5;
	var navbarHeight = $("#js-navbar").outerHeight();
	// on scroll, let the interval function know the user has scrolled
	$(window).scroll(function(event){
	  didScroll = true;
	});
	// run hasScrolled() and reset didScroll status
	setInterval(function() {
	  if (didScroll) {
	    hasScrolled();
	    didScroll = false;
	  }
	}, 250);
	function hasScrolled() {
	   var st = $(this).scrollTop();
	   if (Math.abs(lastScrollTop - st) <= delta) {return;}
  		// If current position > last position AND scrolled past navbar...
		if (st > lastScrollTop && st > navbarHeight){
		  // Scroll Down
		  $("#js-navbar").removeClass("nav-down").addClass("nav-up");
		} else {
		  // Scroll Up
		  // If did not scroll past the document (possible on mac)...
		  if(st + $(window).height() < $(document).height()) { 
		    $("#js-navbar").removeClass("nav-up").addClass("nav-down");
		  }
		}
		lastScrollTop = st;
	}
}
);