fetch("statistics.json")
  .then(response => response.json())
  .then(data => {
    const statsByDate = data["stats_by_date"];

    const dates = Object.keys(statsByDate).sort();
    const infantAvailabilityData = dates.map(date => statsByDate[date]["infant_availability"]);
    const toddlerAvailabilityData = dates.map(date => statsByDate[date]["toddler_availability"]);
    const infantCapacityData = dates.map(date => statsByDate[date]["infant_capacity"]);
    const toddlerCapacityData = dates.map(date => statsByDate[date]["toddler_capacity"]);

    const placesWithCurrentInfantAvailability = data["places_with_infant_availability"]
    const placesWithCurrentToddlerAvailability = data["places_with_toddler_availability"]

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

    const currentInfantAvailabilityList = document.getElementById("infantAvailability");
    if (Array.isArray(placesWithCurrentInfantAvailability)) {
      placesWithCurrentInfantAvailability.forEach(name => {
        const li = document.createElement("li");
        li.textContent = name;
        currentInfantAvailabilityList.appendChild(li);
      });
    } else {
      console.error("No infant availability array found in statistics.json");
    };

    const currentToddlerAvailabilityList = document.getElementById("toddlerAvailability");
    if (Array.isArray(placesWithCurrentToddlerAvailability)) {
      placesWithCurrentToddlerAvailability.forEach(name => {
        const li = document.createElement("li");
        li.textContent = name;
        currentToddlerAvailabilityList.appendChild(li);
      });
    } else {
      console.error("No toddler availability array found in statistics.json");
    };


  })
  .catch(error => console.error("Failed to load data:", error));
