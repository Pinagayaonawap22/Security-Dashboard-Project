document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggleCharts");
  const chartContainer = document.getElementById("chartContainer");

  if (!toggleBtn || !chartContainer) return;

  toggleBtn.addEventListener("click", function () {
    chartContainer.classList.toggle("hidden");

    if (!window.incidentChartCreated && window.incidentData) {
      const ctx = document.getElementById("incidentChart").getContext("2d");

      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Critical", "Resolved", "In Progress", "Escalated"],
          datasets: [{
            data: window.incidentData,
            backgroundColor: [
              "#EF4444", // red
              "#10B981", // green
              "#FACC15", // yellow
              "#6B7280"  // gray
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          cutout: "65%",
          plugins: {
            legend: {
              position: "right",
              labels: {
                color: "#374151",
                font: { size: 14 }
              }
            },
            tooltip: {
              backgroundColor: "#1F2937",
              titleColor: "#fff",
              bodyColor: "#fff",
              padding: 10
            }
          }
        }
      });

      window.incidentChartCreated = true;
    }
  });
});
