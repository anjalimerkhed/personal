document.addEventListener('DOMContentLoaded', function () {
    var intensitySlider = document.getElementById('intensitySlider');
    var textWrapper = document.querySelector('.text-wrapper-4');
  
    intensitySlider.addEventListener('change', function () {
        var intensityValue = intensitySlider.value;
        updateIntensity(intensityValue);
    });
  });
  
  function updateIntensity(value) {
    var textWrapper = document.querySelector('.text-wrapper-19');
    textWrapper.textContent = value + '%';
  
    // Make an HTTP POST request to the Flask API
    fetch('/update_intensity', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ledIntensity: value }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Flask API response:', data);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }
