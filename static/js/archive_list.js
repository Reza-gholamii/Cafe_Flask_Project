function change_status(status) {
    var index = status.classList[3].slice(-1)
    let class_name = status.classList[1]
    let target_name = status.classList[2]
    let target_column = document.getElementById('status' + target_name.slice(-1))
    let target_modal = document.getElementById('modal_status' + target_name.slice(-1))
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
    target_modal.innerText = new_status
    var data = {"index": index, "status": new_status};
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/cashier/' + user_id + '/orders/archive',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (result) {
            console.log("ok", result);
        }, error: function (result) {
            console.log(result);
        }
    });
}


