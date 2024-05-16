 // Function to fetch dust particle data and update HTML
 function updateParticleData() {
  fetch('/dust_particles')
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          const particleContainer = document.getElementById('particle-container');
          particleContainer.innerHTML = ''; // Clear previous data
          for (const id in data) {
              if (data.hasOwnProperty(id)) {
                  const particleData = data[id];
                  const particleBox = document.createElement('div');
                  particleBox.classList.add('particle-box');
                  particleBox.innerHTML = `
                      <h2>Particle ID: ${particleData.id}</h2>
                      <p>Dust Amount: ${particleData.dust} ppm</p>
                  `;
                  particleContainer.appendChild(particleBox);
              }
          }
      })
      .catch(error => console.error('Error fetching dust particle data:', error));
}

// Update particle data initially and set interval to update periodically
updateParticleData();
setInterval(updateParticleData, 5000); // Update every 5 seconds (adjust as needed)