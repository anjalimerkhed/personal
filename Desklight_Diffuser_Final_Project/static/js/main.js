const brightnessInput = document.getElementById('brightness');
const brightnessValue = document.getElementById('brightnessValue');
const lampIcon = document.getElementById('lampIcon');

brightnessInput.addEventListener('input', function () {
    const brightnessLevel = this.value;
    brightnessValue.textContent = brightnessLevel + '%';

    // Change lamp icon based on brightness level
    if (brightnessLevel >= 75) {
        lampIcon.src = '../static/img/dark_led_copy.png';
    } else if (brightnessLevel >= 50) {
        lampIcon.src = '../static/img/light_led_copy.png';
    } else {
        lampIcon.src = '../static/img/white_light_copy.png';
    }
});



// ********************

document.getElementById('toggleButton').addEventListener('click', function () {
    const textElement = document.getElementById('displayText');
    if (textElement.style.display === 'none' || textElement.style.display === '') {
        textElement.style.display = 'block';
    } else {
        textElement.style.display = 'none';
    }

    const diffuser_container = document.getElementById('diffuser_container');
    if (diffuser_container.style.display === 'block' || diffuser_container.style.display === '') {
        diffuser_container.style.display = 'none';
    } else {
        diffuser_container.style.display = 'block';
    }

    const smartled_container = document.getElementById('smartled_container');
    if (smartled_container.style.height === '48vh' || smartled_container.style.height === '') {
        smartled_container.style.height = 'auto';
    } else {
        smartled_container.style.height = '48vh';
    }

    var toggle_icon = document.getElementById('toggle_icon');
    var toggle_icon_expand = document.getElementById('toggle_icon_expand');
    if (toggle_icon.style.display === 'none') {
        toggle_icon.style.display = 'block';
        toggle_icon_expand.style.display = 'none';
    } else {
        toggle_icon.style.display = 'none';
        toggle_icon_expand.style.display = 'block';
    }

});

// ******************************


document.getElementById('toggleButton2').addEventListener('click', function () {

    var textElement2 = document.getElementById('displayText2');
    if (textElement2.style.display === 'none' || textElement2.style.display === '') {
        textElement2.style.display = 'block';
    } else {
        textElement2.style.display = 'none';
    }

    var smartled_container2 = document.getElementById('smartled_container');
    if (smartled_container2.style.display === 'block' || smartled_container2.style.display === '') {
        smartled_container2.style.display = 'none';
    } else {
        smartled_container2.style.display = 'block';
    }

    var diffuser_container2 = document.getElementById('diffuser_container');
    if (diffuser_container2.style.height === '48vh' || diffuser_container2.style.height === '') {
        diffuser_container2.style.height = 'auto';
        diffuser_container2.style.marginTop = '1vh';

    } else {
        diffuser_container2.style.height = '48vh';
    }

    var toggle_icon2 = document.getElementById('toggle_icon2');
    var toggle_icon_expand2 = document.getElementById('toggle_icon_expand2');
    if (toggle_icon2.style.display === 'none') {
        toggle_icon2.style.display = 'block';
        toggle_icon_expand2.style.display = 'none';
    } else {
        toggle_icon2.style.display = 'none';
        toggle_icon_expand2.style.display = 'block';
    }
});


// *********************************

// Function to make POST request to Flask API
function publishColor(color) {
    fetch('/publish-color', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ color: color })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

// Event listener for range input change
document.getElementById('brightness').addEventListener('change', function() {
    var brightness = this.value;

    // Determine color based on brightness value
    var color;
    if (brightness >= 0 && brightness < 33) {
        color = 'White';
    } else if (brightness >= 33 && brightness < 67) {
        color = 'NatureWhite';
    } else {
        color = 'Warm';
    }

    // Publish color to Flask API
    publishColor(color);
});





// code by nikky........
