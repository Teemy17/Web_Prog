document.addEventListener("DOMContentLoaded", function () {
  function generateInitialJson() {
    const table = document.getElementById("originalTable");
    const headers = table.querySelectorAll("thead th");
    const rows = table.querySelectorAll("tbody tr:not(:last-child)");

    let jsonData = {
      Header: [],
      Body: [],
      Footer: [],
    };

    headers.forEach((header) => {
      jsonData.Header.push(header.textContent);
    });

    let total = 0;
    rows.forEach((row) => {
      let rowObj = {};
      const cells = row.querySelectorAll("td");
      cells.forEach((cell, index) => {
        rowObj[`col${index + 1}`] = cell.textContent;
        if (index === cells.length - 1) {
          total += parseFloat(cell.textContent);
        }
      });
      jsonData.Body.push(rowObj);
    });

    jsonData.Footer = [
      {
        value: "Total",
        span: headers.length - 1,
      },
      {
        value: total.toString(),
      },
    ];

    return jsonData;
  }

  function renderTable(jsonData) {
    const table = document.createElement("table");
    table.setAttribute("border", "1");
    table.align = "center";

    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    jsonData.Header.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    jsonData.Body.forEach((row) => {
      const tr = document.createElement("tr");
      Object.values(row).forEach((val) => {
        const td = document.createElement("td");
        td.textContent = val;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    const tfoot = document.createElement("tfoot");
    const footerRow = document.createElement("tr");
    jsonData.Footer.forEach((footer) => {
      const td = document.createElement("td");
      td.textContent = footer.value;
      if (footer.span) {
        td.setAttribute("colspan", footer.span);
      }
      footerRow.appendChild(td);
    });
    tfoot.appendChild(footerRow);
    table.appendChild(tfoot);

    return table;
  }

  function convert() {
    try {
      const newData = JSON.parse(
        document.getElementById("displayTextarea").value
      );
      const newTable = renderTable(newData);
      const container = document.getElementById("newTable");
      container.innerHTML = "";
      container.appendChild(newTable);
    } catch (e) {
      alert("Invalid JSON: " + e.message);
    }
  }

  const initialData = generateInitialJson();
  const textArea = document.getElementById("displayTextarea");
  textArea.value = JSON.stringify(initialData, null, 2);

  document.querySelector(".button button").addEventListener("click", convert);
});
