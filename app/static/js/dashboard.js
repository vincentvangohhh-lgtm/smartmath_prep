document.addEventListener("DOMContentLoaded", function () {
    // Gọi API thống kê từ Backend Flask
    fetch('/api/stats-overview')
        .then(response => response.json())
        .then(data => {
            // Hiển thị AI Insights điểm mạnh yếu
            document.getElementById('strongest-topic').innerText = data.insights.strongest;
            document.getElementById('weakest-topic').innerText = data.insights.weakest;

            // 1. Line Chart: Tiến trình điểm số theo thời gian
            const ctxLine = document.getElementById('lineChart').getContext('2d');
            new Chart(ctxLine, {
                type: 'line',
                data: {
                    labels: data.timeline.labels,
                    datasets: [{
                        label: 'Điểm số đạt được',
                        data: data.timeline.scores,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        borderWidth: 3,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { min: 0, max: 10 }
                    }
                }
            });

            // 2. Radar Chart: Phân tích 7 năng lực chuyên đề Toán THPT
            const ctxRadar = document.getElementById('radarChart').getContext('2d');
            new Chart(ctxRadar, {
                type: 'radar',
                data: {
                    labels: data.radar.labels,
                    datasets: [{
                        label: 'Tỷ lệ chính xác (%)',
                        data: data.radar.data,
                        backgroundColor: 'rgba(25, 135, 84, 0.2)',
                        borderColor: '#198754',
                        pointBackgroundColor: '#198754',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        r: { min: 0, max: 100 }
                    }
                }
            });
        })
        .catch(err => console.error("Lỗi khi tải dữ liệu API Dashboard: ", err));
});