document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/results")
        .then(function (response) { return response.json(); })
        .then(function (data) {
            document.getElementById("total-count").textContent =
                "総回答数: " + data.total + "件";

            if (data.total === 0) {
                document.getElementById("ageChart")
                    .parentElement.innerHTML = '<p class="no-data">まだ回答がありません</p>';
                document.getElementById("foodChart")
                    .parentElement.innerHTML = '<p class="no-data">まだ回答がありません</p>';
                document.getElementById("movie-list").innerHTML =
                    '<p class="no-data">まだ回答がありません</p>';
                return;
            }

            // Age pie chart
            var ageLabels = Object.keys(data.age_groups);
            var ageValues = Object.values(data.age_groups);
            new Chart(document.getElementById("ageChart"), {
                type: "pie",
                data: {
                    labels: ageLabels,
                    datasets: [{
                        data: ageValues,
                        backgroundColor: [
                            "#FF6384", "#36A2EB", "#FFCE56",
                            "#4BC0C0", "#9966FF", "#FF9F40"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: "bottom" }
                    }
                }
            });

            // Food bar chart
            var foodLabels = Object.keys(data.favorite_foods);
            var foodValues = Object.values(data.favorite_foods);
            new Chart(document.getElementById("foodChart"), {
                type: "bar",
                data: {
                    labels: foodLabels,
                    datasets: [{
                        label: "回答数",
                        data: foodValues,
                        backgroundColor: "#4a90d9"
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // Movie list
            var movieList = document.getElementById("movie-list");
            if (data.favorite_movies.length === 0) {
                movieList.innerHTML = '<p class="no-data">まだ回答がありません</p>';
            } else {
                movieList.innerHTML = data.favorite_movies
                    .map(function (movie) {
                        return '<span class="movie-tag">' +
                            movie.replace(/</g, "&lt;").replace(/>/g, "&gt;") +
                            '</span>';
                    })
                    .join("");
            }
        });
});
