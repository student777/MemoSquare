/* report page */
function open_report() {
    window.open("/report/", "", "width=500,height=400");
}
function validate_report(){
    var content = $("#textarea").val();
    if(content.length>0){
        return true;
    }
    else{
        alert('Please check your message!');
        return false;
    }
}