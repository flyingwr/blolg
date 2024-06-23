document.getElementById('fetchData').addEventListener('click', async () => {
    const playerName = document.getElementById('playerName').value;
    if (!playerName) {
        alert('Please enter a player name');
        return;
    }

    try {
        const response = await fetch(`/api/players?player=${playerName}`);
        const data = await response.json();

        if (response.status !== 200) {
            alert(data.error);
            return;
        }

        const champions = new Set();
        data.matches.forEach(match => champions.add(match.title.Champion));
        populateChampionFilter(champions);
        updateTable(data);
    } catch (error) {
        console.error('Error fetching player data:', error);
    }
});

const championFilter = document.getElementById('championFilter');
championFilter.addEventListener('change', () => {
    const playerName = document.getElementById('playerName').value;
    fetchAndUpdateTable(playerName, championFilter.value);
});

async function fetchAndUpdateTable(playerName, champion) {
    if (!playerName) {
        return;
    }

    try {
        const champion_param = champion !== "" ? `&champion=${champion}` : "";
        const response = await fetch(`/api/players?player=${playerName}${champion_param}`);
        const data = await response.json();

        if (response.status !== 200) {
            alert(data.error);
            return;
        }

        updateTable(data);
    } catch (error) {
        console.error('Error fetching player data:', error);
    }
}

function populateChampionFilter(champions) {
    const championFilter = document.getElementById('championFilter');
    championFilter.innerHTML = '<option value="">All Champions</option>';
    champions.forEach(champion => {
        const option = document.createElement('option');
        option.value = champion;
        option.textContent = champion;
        championFilter.appendChild(option);
    });
}

function updateTable(data) {
    const tableBody = document.querySelector('#statsTable tbody');
    tableBody.innerHTML = '';
    const selectedChampion = document.getElementById('championFilter').value;

    data.matches.forEach(match => {
        if (selectedChampion && match.title.Champion !== selectedChampion) {
            return;
        }

        const row = document.createElement('tr');

        const championCell = document.createElement('td');
        championCell.textContent = match.title.Champion;
        row.appendChild(championCell);

        const kdaCell = document.createElement('td');
        kdaCell.textContent = `${match.title.Kills}/${match.title.Deaths}/${match.title.Assists}`;
        row.appendChild(kdaCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = match.title["DateTime UTC"];
        row.appendChild(dateCell);

        const tournamentCell = document.createElement('td');
        tournamentCell.textContent = match.title.OverviewPage;
        row.appendChild(tournamentCell);

        document.getElementById("win_col").textContent = `Win (${data.wins}/${data.defeats}) - ${data.win_rate}% WR`;

        const resultCell = document.createElement('td');
        resultCell.textContent = match.title.PlayerWin;
        resultCell.className = match.title.PlayerWin === 'Yes' ? 'win' : 'loss';
        row.appendChild(resultCell);

        tableBody.appendChild(row);
    });
}
