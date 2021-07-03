function change_status(status) {
    var index = status.getAttribute(("data-recepit"))
    let class_name = status.classList[1]
    let target_name = status.classList[2]
    let target_column = document.getElementById(target_name)

    if (class_name === 'icon_refresh') {
        new_status = 'پرداخت نشده'
    } else if (class_name === 'icon_check') {
        new_status = 'پرداخت شده'
    } else if (class_name === 'icon_trash') {
        new_status = 'کنسل شده'
    }
    target_column.innerText = new_status

    var data = {"recepit_id": index, "status": new_status};

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/cashier/' + user_id + '/recepits',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (result) {
            console.log("ok", result);
        }, error: function (result) {
            console.log(result);
        }
    });
}


