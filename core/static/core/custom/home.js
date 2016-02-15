/**
 * Created by omkar on 13/2/16.
 */

jQuery(document).ready(function() {

    console.log("---document readey----");
    jQuery(".navbar li a").on('click', function() {
        console.log('---clicked-----');
       jQuery('li').removeClass('active');
       jQuery(this).parent('li').toggleClass('active');
    });

    jQuery(".panel-toggle.left").hide();
})