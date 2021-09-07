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

$(document).ready(function () {
    $("#searchInput").on("keyup", function () {
        var value = $(this).val();
        $("#table_body tr").filter(function () {
            $(this).toggle($(this).text().indexOf(value) > -1)
        });
    });
});

$("#unpaid-button").on("click", function () {
    $("#table_body tr").filter(function () {
        $(this).toggle($(this).text().indexOf("پرداخت نشده") > -1)
    });

});

$("#paid-button").on("click", function () {
    $("#table_body tr").filter(function () {
        $(this).toggle($(this).text().indexOf("پرداخت شده") > -1)
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
            var first_row =x.innerHTML;
            var second_row = y.innerHTML;
            if (column === "column0") {
                first_row = Number(x.innerHTML);
                second_row = Number(y.innerHTML);
            }
            if (column === "column1") {
                first_row = Number(x.innerHTML.trim().slice(0, -5));
                second_row = Number(y.innerHTML.trim().slice(0, -5));
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