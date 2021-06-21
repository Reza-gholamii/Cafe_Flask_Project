function change_status(status) {
    let row_number = status.parentNode.parentNode
    let target_column = row_number.childNodes[5]
    let class_name = status.classList[1]
    if (class_name === 'icon_refresh') {
        target_column.innerText = 'جدید'
    } else if (class_name === 'icon_cook') {
        target_column.innerText = 'در حال پخت'
    } else if (class_name === 'icon_serve') {
        target_column.innerText = 'سرو شده'
    } else if (class_name === 'icon_check') {
        target_column.innerText = 'پرداخت شده'
    } else if (class_name === 'icon_trash') {
        target_column.innerText = 'کنسل شده'
    }
}
