var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
var month_name = ['1/2024', '2/2024', '3/2024', '4/2024', '5/2024', '6/2024', '7/2024', '8/2024', '9/2024', '10/2024', '11/2024', '12/2024'];
var StartDate = [1, 4, 5, 1, 3, 6, 1, 4, 0, 2, 5, 0];
var month = 0;

function createCalendar() {
    document.writeln("<table>");

    document.writeln("<thead id='table_head'>");
    document.writeln("<tr>");

    document.writeln("<td style='padding: 0px;'>");
    document.writeln("<button onclick='back()'> &lt; </button>");
    document.writeln("</td>");

    document.writeln("<td colspan='5' id='monthHead'></td>");

    document.writeln("<td style='padding: 0px;'>");
    document.writeln("<button onclick='forward()'> &gt; </button>");
    document.writeln("</td>");

    document.writeln("</tr>");

    document.writeln("<tr>");
    for (var i = 0; i < 7; i++) {
        document.writeln(`<td>${days[i]}</td>`);
    }
    document.writeln("</tr>");

    document.writeln("</thead>");

    document.writeln("<tbody id='tableBody'></tbody>");

    document.writeln("</table>")
}

createCalendar();


function show_monthOf2024(month) {
    document.getElementById("monthHead").innerHTML = month_name[month];

    var table = document.getElementById("tableBody");
    table.innerHTML = "";
    var day = 1;
    var day_of_week = StartDate[month];
    var days_of_month = 31;

    if (month == 1) {
        days_of_month = 29;
    } else if (month == 3 || month == 5 || month == 8 || month == 10) {
        days_of_month = 30;
    }

    for (var i = 0; i < 6; i++) {
        var row = document.createElement("tr");
        var isRowEmpty = true; 

        for (var j = 0; j < 7; j++) {
            var col = document.createElement("td");
            if (i == 0 && j < day_of_week) {
                col.innerHTML = "";
            } else if (day <= days_of_month) {
                col.innerHTML = day;
                day++;
                isRowEmpty = false; 
            }
            row.appendChild(col);
        }

        if (!isRowEmpty) {
            table.appendChild(row);
        }
    }
}


show_monthOf2024(month);

function back() {
    month = (month + 11) % 12;
    document.getElementById("monthHead").innerHTML = month[month];
    show_monthOf2024(month);
}

function forward() {
    month = (month + 1) % 12;
    document.getElementById("monthHead").innerHTML = month[month];
    show_monthOf2024(month);
}