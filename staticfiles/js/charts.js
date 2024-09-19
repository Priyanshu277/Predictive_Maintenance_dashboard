function createTemperatureChart(timestamps, temperatures) {
    const tempCtx = document.getElementById('temperatureChart').getContext('2d');
    new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: timestamps.map(t => new Date(t)),
            datasets: [{
                label: 'Temperature',
                data: temperatures,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createVibrationChart(timestamps, vibrations) {
    const vibCtx = document.getElementById('vibrationChart').getContext('2d');
    new Chart(vibCtx, {
        type: 'line',
        data: {
            labels: timestamps.map(t => new Date(t)),
            datasets: [{
                label: 'Vibration',
                data: vibrations,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createScatterChart(scatterData) {
    const scatterCtx = document.getElementById('scatterChart').getContext('2d');
    new Chart(scatterCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Temperature vs Vibration',
                data: scatterData.map(point => ({
                    x: point.x,
                    y: point.y
                })),
                backgroundColor: 'rgb(75, 192, 192)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temperature'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Vibration'
                    }
                }
            }
        }
    });
}