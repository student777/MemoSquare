$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/category/?format=html",
        xhrFields: {
            withCredentials: true // for authentication
        },
        success: function (response) {
            $('#category-list').append($(response).filter("#response1").html());
            $('#modals').append($(response).filter("#response2").html());
            $('#nav-bar').append($(response).filter("#response3").html());

            // Initialize modal
            $('.modal').modal();

            // Refresh page when category edit/remove modal closed
            $('#category-modal').modal({
                complete: function () {
                    location.href = '';
                }
            });

            // Initialize side mobile nav-bar
            $(".button-collapse").sideNav();

            // Check category radio
            // if category is empty string,  let radio box id="radio" named 'All' memos be checked...?
            $("#radio" + category_id).prop('checked', true);
        },
        error: function (response) {
            console.log(response);
        }
    });
});