import { Chart } from "@/components/ui/chart"
document.addEventListener("DOMContentLoaded", () => {
  // Initialize chart
  initDocumentChart()
})

// Initialize document type chart
function initDocumentChart() {
  const chartCanvas = document.getElementById("document-types-chart")
  if (!chartCanvas) return

  // Count documents by category
  const documents = document.querySelectorAll(".document-tile")
  const categories = {}

  documents.forEach((doc) => {
    const category = doc.querySelector(".document-category").textContent
    if (categories[category]) {
      categories[category]++
    } else {
      categories[category] = 1
    }
  })

  // Create chart
  createDocumentChart(chartCanvas, categories)
}

// Create document type chart
function createDocumentChart(canvas, categories) {
  // Define colors for categories
  const categoryColors = {
    invoice: "#1e88e5",
    contract: "#43a047",
    resume: "#ff9800",
    report: "#9c27b0",
  }

  // Prepare data for chart
  const labels = Object.keys(categories)
  const data = Object.values(categories)
  const backgroundColor = labels.map((label) => categoryColors[label] || "#6c757d")

  // Create chart
  window.documentChart = new Chart(canvas, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: backgroundColor,
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            font: {
              size: 14,
            },
            padding: 20,
          },
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || ""
              const value = context.raw || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = Math.round((value / total) * 100)
              return `${label}: ${value} (${percentage}%)`
            },
          },
        },
      },
    },
  })
}

// Update document chart with new data
function updateDocumentChart(categories) {
  if (!window.documentChart) {
    const chartCanvas = document.getElementById("document-types-chart")
    if (chartCanvas) {
      createDocumentChart(chartCanvas, categories)
    }
    return
  }

  // Define colors for categories
  const categoryColors = {
    invoice: "#1e88e5",
    contract: "#43a047",
    resume: "#ff9800",
    report: "#9c27b0",
  }

  // Update chart data
  window.documentChart.data.labels = Object.keys(categories)
  window.documentChart.data.datasets[0].data = Object.values(categories)
  window.documentChart.data.datasets[0].backgroundColor = window.documentChart.data.labels.map(
    (label) => categoryColors[label] || "#6c757d",
  )

  // Update chart
  window.documentChart.update()
}

