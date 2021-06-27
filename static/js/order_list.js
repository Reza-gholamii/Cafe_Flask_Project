function change_status(status) {
    let new_status = ""
    let row_number = status.parentNode.parentNode
    let target_column = row_number.childNodes[5]
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
