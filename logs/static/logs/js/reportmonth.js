function showDayLog(day,id_user){
    $(".active-log").removeClass("active-log");
    //$(".active-log-link").removeClass("active-log-link");
    if($("#log-"+day+"-"+id_user).length > 0){
        $("#log-"+day+"-"+id_user).addClass("active-log");
    }
    //$("#daylog-"+day).addClass("active-log-link");
}

function showDayGap(day,id_user){
    $(".active-log").removeClass("active-log");
    //$(".active-log-link").removeClass("active-log-link");
    if($("#gap-"+day+"-"+id_user).length > 0){
        $("#gap-"+day+"-"+id_user).addClass("active-log");
    }
    //$("#daylog-"+day).addClass("active-log-link");
}

function showDayPresence(day){
    $(".active-day").removeClass("active-day");
    $(".active-day-link").removeClass("active-day-link");
    if($("#presence-day-"+day).length > 0){
        $("#presence-day-"+day).addClass("active-day");
    }
    $("#day-"+day).addClass("active-day-link");

}

