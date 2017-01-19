/* report page */
function open_report() {
    window.open("/report/", "", "width=500,height=400");
}
function send_report(){
    var content = $("#textarea").val();
    if(content.length>0){
        var url = "/report/";
        var settings = {
            method: 'POST',
            data: {
                "content": content,
            },
            success: function (response){
                alert('소중한 의견 감사합니다!');
                 $('#report-modal').modal('close');
            },
            error: function (response) {
                console.log(response);
            }
        };
        $.ajax(url, settings);
    }
    else{
        alert('Please check your message!');
    }
}