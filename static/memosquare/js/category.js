function delete_category(pk, caller) {
    if (confirm('really?')) {
        var settings = {
            type: 'DELETE',
            success: function success(result, status, xhr) {
                $(caller).parent().parent().remove();
            },
            error: function (response) {
                console.log(response);
            }
        };
        var url = '/category/' + pk + '/';
        $.ajax(url, settings);
    }
}

function edit_category(pk, caller){
    var url = '/category/' + pk + '/';
    var category_name = $(caller).parent().parent().children().children().get(0).value;
    if(category_name.length>0){
        var settings = {
            method: 'POST',
            data: {
                name: category_name,
            },
            success: function (response) {
                alert('saved');
                console.log(response);
            },
            error: function (response) {
                console.log(response);
            }
        };
        $.ajax(url, settings);
    }
    else{
        alert('Category name should be at least 1 characters');
    }
}

function add_category(){
    var category_name = $("#add-category-modal input").val();
    if(category_name.length>0){
        var url = "/category/";
        var settings = {
            method: 'POST',
            data: {
                name: category_name,
            },
            success: function (response){
                location.href='/memo/?category_pk=' + response.pk;
            },
            error: function (response) {
                console.log(response);
            }
        };
        $.ajax(url, settings);
    }
    else{
        alert('Category name should be at least 1 characters');
    }
}