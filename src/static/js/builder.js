$(document).ready(function(){
    const formatCash = n => {
        if (n < 1e3) return n;
        if (n >= 1e3 && n < 1e6) return +(n / 1e3).toFixed(1) + "K";
        if (n >= 1e6 && n < 1e9) return +(n / 1e6).toFixed(1) + "M";
        if (n >= 1e9 && n < 1e12) return +(n / 1e9).toFixed(1) + "B";
        if (n >= 1e12) return +(n / 1e12).toFixed(1) + "T";
    };

    function createBuildInfo(data){
        return `
            <h3>Overall: ${data.overall}</h3>
            <h3>Remaining: €${formatCash(data.remaining)}</h3>
            <h3>Spent: €${formatCash(data.spent)}</h3>
        `
    }

    function showSpinner(){
        const spinner = `
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
        `
        $("#spinner").html(spinner);
    }

    function hideSpinner(){
        $("#spinner").empty();
    }

    function createTableRow(player){
        const cash = formatCash(player.value);
        return `
            <tr>
                <td>${player.name}</td>
                <td>${player.nationality}</td>
                <td>${player.club}</td>
                <td>
                    <img src="${player.photo}" alt="${player.photo}" />
                </td>
                <td>${player.overall}</td>
                <td>${player.position}</td>
                <td>€${cash}</td>
            </tr>
        `;
    }

    function createTable(players){
        let tableDiv = `
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Nationality</th>
                    <th>Club</th>
                    <th>Photo</th>
                    <th>Overall</th>
                    <th>Position</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
        `
        for(let player of players){
            tableDiv += createTableRow(player);
        }
        tableDiv += "</tbody>";
        return tableDiv;
    }

    $("#build_btn").on("click", function(){
        const data = new FormData();
        data.append("budget", $("#budget").val());
        $("#players").empty();
        $("#build_info").empty();
        showSpinner();
        $.ajax({
            type: 'POST',
            url: '/builder',
            data,
            processData: false,
            contentType: false
        })
        .done(function(data){
            const table = createTable(data.team);
            $("#players").html(table);
            const buildInfo = createBuildInfo(data);
            $("#build_info").html(buildInfo);
            hideSpinner();
        })
        .fail(function(err){
            console.log(err);
            hideSpinner();
        })
    })
});