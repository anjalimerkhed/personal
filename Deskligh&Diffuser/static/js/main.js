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
var selectedButtonClass = ''; // Variable to store selected button class

function displayImage(imageNumber) {
    // Hide all images
    document.getElementById('image1').style.display = 'none';
    document.getElementById('image2').style.display = 'none';
    document.getElementById('image3').style.display = 'none';

    // Show the selected image
    var imageId = 'image' + imageNumber;
    var selectedImage = document.getElementById(imageId);
    if (selectedImage) {
        selectedImage.style.display = 'block';
    } else {
        console.error('Image not found');
    }

    // Determine color based on displayed image
    var color = determineColor();

    // Publish color to Flask API
    publishColor(color);

}

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
function determineColor() {
    var color;
    if (document.getElementById('image1').style.display === 'block') {
        color = 'Warm';
    } else if (document.getElementById('image2').style.display === 'block') {
        color = 'NatureWhite';
    } else {
        color = 'White';
    }
    return color;
}


$("#roundslider2").roundSlider({
    sliderType: "min-range",
    value: 0,
    circleShape: "half-right",
    width: 8,
    handleSize: "+15",
    change: function (event) {
        var newValue = event.value;
        updateIntensityAPI(newValue);
    }
});

$("#roundslider2 .rs-tooltip").addClass('smartlight_value');

$("#roundslider3").roundSlider({
    sliderType: "min-range",
    value: 3, // Starting value
    min: 1, // Minimum value
    max: 4, // Maximum value
    circleShape: "half-right",
    width: 8,
    handleSize: "+15"
});
$("#roundslider3 .rs-tooltip").addClass('diffuser_value');


function updateIntensityAPI(intensity) {
    $.ajax({
        url: '/update_intensity',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ ledIntensity: intensity }),
        success: function (response) {
            console.log(response);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}
var textWrapper = document.querySelector('.smartlight_value');


function updateLEDState(previousIntensity, previousColor) {

    document.getElementById('White').style.border = 'none';
    document.getElementById('Warm').style.border = 'none';
    document.getElementById('NatureWhite').style.border = 'none';
    // Hide all images
    document.getElementById('image1').style.display = 'none';
    document.getElementById('image2').style.display = 'none';
    document.getElementById('image3').style.display = 'none';

    if (previousColor == "1") {
        document.getElementById('White').style.border = '2px solid rgb(156, 152, 152)';
        document.getElementById('image3').style.display = 'block';
    } else if (previousColor == "2") {
        document.getElementById('Warm').style.border = '2px solid rgb(156, 152, 152)';
        document.getElementById('image1').style.display = 'block';
    } else {
        document.getElementById('NatureWhite').style.border = '2px solid rgb(156, 152, 152)';
        document.getElementById('image2').style.display = 'block';
    }

    const intensityPercentage = (previousIntensity / 255) * 100;
    textWrapper.textContent = Math.round(intensityPercentage);
    $("#roundslider2").roundSlider("option", "value", Math.round(intensityPercentage));                                                                                             
}


var socket;
var ip;

fetch("../static/js/local.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)

        socket.on('connect', function () {
            console.log("connected");
        });


        // Event listener for receiving LED state updates
        socket.on('desklight', function (data) {
            // Update UI with received LED state
            updateLEDState(data.intensity, data.color);
        });
    })




