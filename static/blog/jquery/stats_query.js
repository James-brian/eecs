$(document).ready(function() {
$("#target1").css("color", "");
$("#target1").prop("disabled", true);
$("#target4").remove();
$("#target2").appendTo("#right-well");
$("#target5").clone().appendTo("#left-well");
$("#target1").parent().css("background-color", "red");
$("#right-well").children().css("color", "blue");
$("#left-well").children().css("color", "green");
$(".target:nth-child(2)").addClass("animated bounce");
$(".target:even").addClass("animated shake");
/* $("body").addClass("animated fadeOut"); */
});

