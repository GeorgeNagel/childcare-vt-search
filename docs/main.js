fetch("statistics.json")
  .then(response => response.json())
  .then(data => {
    const availability = data.availability;

    const dates = Object.keys(availability).sort();
    const infantData = dates.map(date => availability[date].infant);
    const toddlerData = dates.map(date => availability[date].toddler);

    const ctx = document.getElementById('availabilityChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Infant',
            data: infantData,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false,
          },
          {
            label: 'Toddler',
            data: toddlerData,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Vacancies' }, beginAtZero: true }
        }
      }
    });
  })
  .catch(error => console.error("Failed to load data:", error));
