$("[data-id=adder_num]").bind('click', function () {
    let num = Number($(this).parent().children('b')[0].innerText);
    $(this).parent().children('b')[0].innerText = String(num + 1);
})

$("[data-id=suber_num]").bind('click', function () {
    let num = Number($(this).parent().children('b')[0].innerText);
    if (num !== 1) {
        $(this).parent().children('b')[0].innerText = String(num - 1);
    }
})


function change_status(status) {
    let new_status = ""
    let row_number = status.parentNode.parentNode
    let row_id = row_number.classList[1]
    if (row_id === 'row-recepit') {
        var target_column = row_number.childNodes[7];
    } else {
        var target_column = row_number.childNodes[5];
    }

    let class_name = status.classList[1]
    if (class_name === 'icon_refresh') {
        new_status = 'جدید'
    } else if (class_name === 'icon_cook') {
        new_status = 'در حال پخت'
    } else if (class_name === 'icon_serve') {
        new_status = 'سرو شده'
    } else if (class_name === 'icon_check') {
        new_status = 'پرداخت شده'
    } else if (class_name === 'icon_trash') {
        new_status = 'کنسل شده'
    }
    target_column.innerText = new_status
    var data = {"status": new_status};

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/cashier/orders',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (result) {
            console.log("ok", result);
        }, error: function (result) {
            console.log(result);
        }
    });
}
