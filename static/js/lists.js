function change_status(status) {
    let target_column = document.getElementById('status1')
    if (status.id === 'icon_refresh') {
        target_column.innerText = 'جدید'
    } else if (status.id === 'icon_cook') {
        target_column.innerText = 'در حال پخت'
    } else if (status.id === 'icon_serve') {
        target_column.innerText = 'سرو شده'
    } else if (status.id === 'icon_check') {
        target_column.innerText = 'پرداخت شده'
    } else if (status.id === 'icon_trash') {
        target_column.innerText = 'کنسل شده'
    }
}


