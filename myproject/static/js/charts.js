function createPlayerCharts(containerId, labels, playersData) {

    const container = document.getElementById(containerId);

    Object.keys(playersData).forEach(playerName => {

        const canvas = document.createElement("canvas");
        container.appendChild(canvas);

        new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Points",
                        data: playersData[playerName].points,
                        borderColor: "#4bc0c0",
                        fill: false
                    }
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: playerName,
                        color: "#fff"
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    });
}

const t1Labels = JSON.parse(document.getElementById("t1-labels").textContent);
const t1Data   = JSON.parse(document.getElementById("t1-data").textContent);

const t2Labels = JSON.parse(document.getElementById("t2-labels").textContent);
const t2Data   = JSON.parse(document.getElementById("t2-data").textContent);

createPlayerCharts("team1-charts", t1Labels, t1Data);
createPlayerCharts("team2-charts", t2Labels, t2Data);
