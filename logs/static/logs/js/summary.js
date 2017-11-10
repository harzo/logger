function showDayLog(day){
    $(".active-log").removeClass("active-log");
    $(".active-log-link").removeClass("active-log-link");
    if($("#log-"+day).length > 0){
        $("#log-"+day).addClass("active-log");
    }
    $("#daylog-"+day).addClass("active-log-link");
}

function showDayGap(day){
    $(".active-log").removeClass("active-log");
    $(".active-log-link").removeClass("active-log-link");
    if($("#gap-"+day).length > 0){
        $("#gap-"+day).addClass("active-log");
    }
    $("#daylog-"+day).addClass("active-log-link");
}

$( document ).ready(function() {
    /*$('div[id^=log-]').each(function(){
        $("#day"+$(this).attr('id')+" span").css("color","white");
        $("#day"+$(this).attr('id')+" .dl-hours").html("5.5h");
    })*/

    $('div[id^=log-]').last().addClass('active-log');
});

