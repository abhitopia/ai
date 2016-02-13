(function($){

	"use strict";

	/* ---------------------------------------------- /*
	 * Insert switcher into body
	/* ---------------------------------------------- */

	var $code = '<link id="style_switcher" href="" rel="stylesheet" type="text/css">\
		<div class="custom-panel" style="left: -230px;">\
	<div class="panel-options">\
		<p>Choose Layout Sample</p>\
		<p><a class="st-sw-layout" href="index.html"><i class="fa fa-angle-right"></i> Single Image- Light</a>\
		<a class="st-sw-layout" href="index-2.html"><i class="fa fa-angle-right"></i> Single Image- Dark</a>\
		<a class="st-sw-layout" href="index-3.html"><i class="fa fa-angle-right"></i> Surface Shader</a>\
		<a class="st-sw-layout" href="index-4.html"><i class="fa fa-angle-right"></i> Youtube</a>\
		<a class="st-sw-layout" href="index-5.html"><i class="fa fa-angle-right"></i> Youtube + Sound</a>\
		<a class="st-sw-layout" href="index-6.html"><i class="fa fa-angle-right"></i> Slideshow</a></p>\
		<p>Choose accent color</p>\
		<ul class="color-picker clearfix">\
			<li><a class="color-1" data-color-name="blue" href="#"></a></li>\
			<li><a class="color-2" data-color-name="green" href="#"></a></li>\
			<li><a class="color-3" data-color-name="alizarin" href="#"></a></li>\
			<li><a class="color-4" data-color-name="concrete" href="#"></a></li>\
			<li><a class="color-5" data-color-name="emerald" href="#"></a></li>\
		</ul>\
	</div>\
	<div class="panel-toggle left">\
		<i class="fa fa-cog"></i>\
	</div>\
</div>\
		</div>';

	/* ---------------------------------------------- /*
	 * Insert switcher into body
	/* ---------------------------------------------- */

	$(document).ready(function () {

		$('.wrapper').after($code);

		$('.color-picker a').click(function(event) {
			event.preventDefault();
			$('.color-picker a').removeClass('selected-color');
			$(this).addClass('selected-color');
			var color_name = $(this).attr('data-color-name');
			$('#style_switcher').attr('href', 'assets/css/colors/' + color_name + '.css');
		});

		/* ---------------------------------------------- /*
		 * Hide panel after 2 seconds
		/* ---------------------------------------------- */

		$('.custom-panel').delay(2000).animate({left: '-230px'}, 250);

		/* ---------------------------------------------- /*
		 * Panel toggle
		/* ---------------------------------------------- */

		$('.panel-toggle').on('click', function() {
			var $panel = $('.custom-panel');
			var left = -230;

			if (parseInt($panel.css('left')) == left) {
				$panel.animate({left: '0px'}, 250);
			} else if ( parseInt($panel.css('left')) == 0) {
				$panel.animate({left: '-230'}, 250);
			}
		});

	});

})(jQuery);