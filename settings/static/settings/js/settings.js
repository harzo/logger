$( document ).ready(function() {

    showHideGapFields();

    $('#id_type').change(function(){
        showHideGapFields();
    });
});

function showHideGapFields(){
    if($('#id_type').val()=="1"){
        $('#gap_weekday').css('display','block');
        $('#gap_end').css('display','initial');
    }
    else if($('#id_type').val()=="2"){
        $('#gap_weekday').css('display','none');
        $('#gap_end').css('display','none');
    }
    else if($('#id_type').val()=="3"){
        $('#gap_weekday').css('display','none');
        $('#gap_end').css('display','initial');
    }
}

