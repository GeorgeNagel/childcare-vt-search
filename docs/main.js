fetch("statistics.json")
  .then(response => response.json())
  .then(data => {
    const statsByDate = data["stats_by_date"];

    const dates = Object.keys(statsByDate).sort();
    const infantAvailabilityData = dates.map(date => statsByDate[date]["infant_availability"]);
    const toddlerAvailabilityData = dates.map(date => statsByDate[date]["toddler_availability"]);
    const infantCapacityData = dates.map(date => statsByDate[date]["infant_capacity"]);
    const toddlerCapacityData = dates.map(date => statsByDate[date]["toddler_capacity"]);

    const ctx = document.getElementById('childcareStatsByDateChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Infant Availability',
            data: infantAvailabilityData,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false,
          },
          {
            label: 'Toddler Availability',
            data: toddlerAvailabilityData,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false,
          },
          {
            label: 'Infant Capacity',
            data: infantCapacityData,
            borderColor: 'rgb(255, 119, 52)',
            backgroundColor: 'rgba(206, 140, 34, 0.2)',
            fill: false,
          },
          {
            label: 'Toddler Capacity',
            data: toddlerCapacityData,
            borderColor: 'rgb(202, 93, 245)',
            backgroundColor: 'rgba(180, 21, 191, 0.2)',
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Total Spots' }, beginAtZero: true }
        }
      }
    });
  })
  .catch(error => console.error("Failed to load data:", error));
