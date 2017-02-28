$(function() {
	var lastScroll = 0;
	var heightRestrict = $(window).height() / 2;
	console.log(heightRestrict);
	$(window).scroll(function() {
		var scrollTop = $(window).scrollTop();
		if (Math.abs(scrollTop - lastScroll) > 5 && scrollTop < heightRestrict) {
			console.log('inside');
			lastScroll = scrollTop;
			var div = 5;
			$(".slowScroll").css({
				"background-position":"0px -"+scrollTop/div+"px"
			});
		}
	});
});