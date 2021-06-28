$(document).ready(function () {
    $(".edit_form").submit(function (event) {
        event.preventDefault();
        var index = $(this).attr("data-index")
        var $inputs = $('#edit_form' + index + ' :input');
        var values = {};
        $inputs.each(function () {
            values[this.name] = $(this).val();
        });

        $("#row_h6_" + index).text(values["name"])
        $("#row_span_" + index).text(values["price"])
        var data = {"action": "update", "name": values["name"], "price": values["price"]};
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/cashier/menu',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (result) {
                console.log("ok", result);
            }, error: function (result) {
                console.log(result);
            }
        });
        $("#edit" + index).modal('hide');
    });


});



