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

    let order_id = status.getAttribute("data-order")

    var data = {
        "order_id": order_id,
        "status": new_status
    };
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/cashier/' + user_id + '/orders/cooking',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (result) {
            console.log("ok", result);
        }, error: function (result) {
            console.log(result);
        }
    });
}


$(document).ready(function () {
    $("#searchInput").on("keyup", function () {
        var value = $(this).val();
        $("#table_body tr").filter(function () {
            $(this).toggle($(this).text().indexOf(value) > -1)
        });
    });
});

$("#first_item-button").on("click", function () {
    $("#table_body tr").filter(function () {
        $(this).toggle($(this).text().indexOf("قهوه") > -1)
    });

});

$("#second_item-button").on("click", function () {
    $("#table_body tr").filter(function () {
        $(this).toggle($(this).text().indexOf("پپرونی") > -1)
    });

});

$("#third_item-button").on("click", function () {
    $("#table_body tr").filter(function () {
        $(this).toggle($(this).text().indexOf("کاپوچینو") > -1)
    });

});

$("#archive-button").on("click", function () {
    $("#table_body tr").show()
});

function sort_data(column) {
    let n = Number(column.slice(-1))
    let table = document.getElementById("main-table");
    let rows = table.rows;
    let target_column = document.getElementById(column);
    let dir = target_column.getAttribute('data-dir')
    for (i = 1; i < (rows.length - 1); i++) {
        for (j = 1; j < (rows.length - 1); j++) {
            let x = rows[j].getElementsByTagName("TD")[n];
            let y = rows[j + 1].getElementsByTagName("TD")[n];
            var first_row = x.innerHTML;
            var second_row = y.innerHTML;
            if (column === "column0" || column === "column1") {
                first_row = Number(x.innerHTML);
                second_row = Number(y.innerHTML);
            }
            if (column === "column3") {
                first_row = Number(x.innerHTML.trim().slice(0, -4));
                second_row = Number(y.innerHTML.trim().slice(0, -4));
            }
            if (dir === "asc") {
                if (first_row > second_row) {
                    rows[j].parentNode.insertBefore(rows[j + 1], rows[j]);
                }
            }
            if (dir === "desc") {
                if (first_row < second_row) {
                    rows[j].parentNode.insertBefore(rows[j + 1], rows[j]);
                }
            }


        }
    }
    if (dir === "desc") {
        target_column.setAttribute("data-dir", "asc")
    } else {
        target_column.setAttribute("data-dir", "desc")
    }
}





