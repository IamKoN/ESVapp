$(document).ready(function() {
  $(".esv_popout").toggle(
    function(){ $(this).next(".esv_lookup").fadeIn(100); },
    function(){ $(this).next(".esv_lookup").fadeOut(100); }
  );
});
