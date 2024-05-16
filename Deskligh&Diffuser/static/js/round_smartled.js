document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.getElementById("root2");
    const rangeInput = document.getElementById("rangeInput");
    const valueDisplay2 = document.getElementById("valueDisplay2");

    const updateValueDisplayPosition2 = function (value) {
        const sliderElement = document.querySelector(".rs-container");
        const radius = parseFloat(sliderElement.getAttribute("r"));
        const angle = (value * 380) / 100;
        const x = radius * Math.cos((angle * Math.PI) / 180);
        const y = radius * Math.sin((angle * Math.PI) / 180);
        const sliderRect = sliderElement.getBoundingClientRect();
        const centerX = sliderRect.left + sliderRect.width / 2;
        const centerY = sliderRect.top + sliderRect.height / 2;
        // const valueX = centerX + x - valueDisplay2.offsetWidth / 2;
        // const valueY = centerY + y - valueDisplay2.offsetHeight / 2;
        // valueDisplay2.style.left = `${valueX}px`;
        // valueDisplay2.style.top = `${valueY}px`;
    };

    // const update = function (e) {
    //     const value = e.value;
    //     // valueDisplay2.innerText = ""; 
    //     // valueDisplay2.appendChild(document.createTextNode(value + "%")); 
    //     updateValueDisplayPosition2(value);
    // };



    const update = function (slider) {
        const value = slider.value;
        // console.log(value);

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
    };


    var intensitySlider = document.getElementById('rangeInput');
    var textWrapper = document.querySelector('.smartlight_value');

    intensitySlider.addEventListener('change', function () {
        update(this); // Pass the slider element itself to the update function
        var intensityValue = intensitySlider.value;
        updateIntensity(intensityValue);
    });


    function updateIntensity(value) {
        var textWrapper = document.querySelector('.smartlight_value');
        textWrapper.textContent = value + '%';
    }


    const renderSemicircularSlider = function (initialValue) {
        $(sliderContainer).roundSlider({
            radius: 100, // Set radius to auto
            width: 8,
            handleSize: "+20",
            startAngle: 0,
            endAngle: 380,
            sliderType: "min-range",
            svgMode: true,
            change: update,
            // drag: update,
            // circleShape: "half-top",
            pathColor: "#a5a5a5",
            circleShape: "half-right",
            value: initialValue

        });
        const handleElement2 = $(sliderContainer).find(".rs-handle")[0];
        const sliderElement = $(sliderContainer).find(".rs-container")[0];
        const sliderTrackElement = sliderElement.querySelector(".rs-bg-color");
        handleElement2.setAttribute("class", handleElement2.getAttribute("class") + " smartlight");

        const smartlight_value = $(sliderContainer).find(".rs-tooltip")[0];
        smartlight_value.setAttribute("class", smartlight_value.getAttribute("class") + " smartlight_value");

        // Find the span element
        // Get the span element
        const spanElement = document.querySelector(".smartlight_value");

        // Get the current content (assuming it's a number)
        const currentValue = parseFloat(spanElement.textContent);

        // Update the content with the new value and keep "%" constant


    };

    renderSemicircularSlider();
});


var socket;
var ip;

fetch("../static/js/local.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        // console.log('ip : ', ip)
        socket = io.connect(ip)

        socket.on('connect', function () {
            // socket.send('a');
            // console.log("connected");
        });


        // Event listener for receiving LED state updates
        socket.on('desklight', function (data) {
            // Update UI with received LED state
            updateLEDState(data.intensity);
        });
        var textWrapper = document.querySelector('.smartlight_value');
        // Function to update UI with LED state
        function updateLEDState(previousIntensity) {
            console.log(previousIntensity);
            // Adjust the intensity value from the range 0-255 to 0-100
            const intensityPercentage = (previousIntensity / 255) * 100;

            // Update UI elements with previous LED state
            textWrapper.textContent = Math.round(intensityPercentage);

            // renderSemicircularSlider(intensityPercentage);

        }

        

    })
    