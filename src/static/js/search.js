$(document).ready(function(){
    const formatCash = n => {
        if (n < 1e3) return n;
        if (n >= 1e3 && n < 1e6) return +(n / 1e3).toFixed(1) + "K";
        if (n >= 1e6 && n < 1e9) return +(n / 1e6).toFixed(1) + "M";
        if (n >= 1e9 && n < 1e12) return +(n / 1e9).toFixed(1) + "B";
        if (n >= 1e12) return +(n / 1e12).toFixed(1) + "T";
    };

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

    $("#search_btn").on("click", function(){
        const data = new FormData();
        data.append("word", $("#word").val());
        showSpinner();
        $("#players").empty();
        $.ajax({
            type: 'POST',
            url: '/',
            data,
            processData: false,
            contentType: false
        })
        .done(function(players){
            const table = createTable(players);
            $("#players").html(table);
            hideSpinner();
        })
        .fail(function(err){
            console.log(err);
            hideSpinner();
        })
    })
});