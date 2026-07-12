function renderTrendChart({
  elementId, labels, data, label, borderColor, backgroundColor, maxValue, valueFormatter,
}) {
  return new Chart(document.getElementById(elementId), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        fill: true,
        tension: 0.3,
      }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          max: maxValue,
          ticks: { callback: valueFormatter },
        },
      },
    },
  })
}
