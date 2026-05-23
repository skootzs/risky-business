// LOAD PERFORMANCE DATA
fetch("data/performance.json")
    .then(response => response.json())
    .then(data => {

        const labels = data.map(
            row => row.date
        );

        const strategy = data.map(
            row => row.strategy_cumulative
        );

        const spy = data.map(
            row => row.spy_cumulative
        );

        new Chart(
            document.getElementById("performanceChart"),
            {
                type: "line",

                data: {
                    labels: labels,

                    datasets: [
                        {
                            label: "Risky Business Strategy",
                            data: strategy,
                            borderColor: "#38bdf8",
                            backgroundColor: "rgba(56,189,248,0.1)",
                            borderWidth: 3,
                            tension: 0.3
                        },

                        {
                            label: "SPY Benchmark",
                            data: spy,
                            borderColor: "#94a3b8",
                            backgroundColor: "rgba(148,163,184,0.08)",
                            borderWidth: 2,
                            tension: 0.3
                        }
                    ]
                },

                options: {
                    responsive: true,

                    plugins: {
                        legend: {
                            labels: {
                                color: "#e5e7eb"
                            }
                        }
                    },

                    scales: {
                        x: {
                            ticks: {
                                color: "#94a3b8"
                            },

                            grid: {
                                color: "rgba(148,163,184,0.08)"
                            }
                        },

                        y: {
                            ticks: {
                                color: "#94a3b8"
                            },

                            grid: {
                                color: "rgba(148,163,184,0.08)"
                            }
                        }
                    }
                }
            }
        );
    });

// FEATURE IMPORTANCE

fetch("data/feature_importance.json")
    .then(response => response.json())
    .then(data => {

        const labels = data.map(
            row => row.feature
        );

        const values = data.map(
            row => row.importance
        );

        new Chart(
            document.getElementById("featureChart"),
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [
                        {
                            label: "Importance",
                            data: values
                        }
                    ]
                },

                options: {
                    responsive: true
                }
            }
        );
    });

let stockData = [];

fetch("data/latest_picks.json")
    .then(response => response.json())
    .then(data => {
        stockData = data;
        renderStockTable();
    });

function renderStockTable() {
    const tbody = document.querySelector("#stockTable tbody");
    const scoreFilter = parseFloat(
        document.getElementById("scoreFilter").value
    );
    const sortBy = document.getElementById("sortSelect").value;

    document.getElementById("scoreValue").textContent =
        scoreFilter.toFixed(2);

    tbody.innerHTML = "";

    const filteredData = stockData
        .filter(stock => stock.predicted_score >= scoreFilter)
        .sort((a, b) => b[sortBy] - a[sortBy]);

    filteredData.forEach(stock => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${stock.ticker}</td>
            <td>${stock.predicted_score.toFixed(2)}</td>
            <td>${(stock.return_5d * 100).toFixed(2)}%</td>
            <td>${(stock.return_20d * 100).toFixed(2)}%</td>
            <td>${(stock.volatility_20d * 100).toFixed(2)}%</td>
        `;

        row.addEventListener("click", () => {
            alert(
                `${stock.ticker}\n\n` +
                `Predicted Score: ${stock.predicted_score.toFixed(2)}\n` +
                `5D Return: ${(stock.return_5d * 100).toFixed(2)}%\n` +
                `20D Return: ${(stock.return_20d * 100).toFixed(2)}%\n` +
                `Volatility: ${(stock.volatility_20d * 100).toFixed(2)}%`
            );
        });

        tbody.appendChild(row);
    });
}

document.getElementById("scoreFilter").addEventListener(
    "input",
    renderStockTable
);

document.getElementById("sortSelect").addEventListener(
    "change",
    renderStockTable
);