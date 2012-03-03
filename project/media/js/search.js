$(document).ready(function(){ 			

	$("#search-area").click(
        function(){
            $("#search-text-box").focus();
        }
      );
      
      $("#search-text-box").focus(
        function(){
            if($(this).val() == "Type Keywords"){
                $(this).val("");
            } 
      }).blur(
        function(){
            if($(this).val() == ""){
                $(this).val("Type Keywords");
            }
      });
});