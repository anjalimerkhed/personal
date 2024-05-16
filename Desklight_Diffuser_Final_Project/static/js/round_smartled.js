document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.getElementById("root2");
    const rangeInput = document.getElementById("rangeInput");
    const valueDisplay2 = document.getElementById("valueDisplay2");

    const updateValueDisplayPosition2 = function (value) {
        const sliderElement = document.querySelector(".rs-container");
        const radius = parseFloat(sliderElement.getAttribute("r"));
        const angle = (value * 380) / 100; // Convert percentage to angle
        const x = radius * Math.cos((angle * Math.PI) / 180);
        const y = radius * Math.sin((angle * Math.PI) / 180);
        const sliderRect = sliderElement.getBoundingClientRect();
        const centerX = sliderRect.left + sliderRect.width / 2;
        const centerY = sliderRect.top + sliderRect.height / 2;
        const valueX = centerX + x - valueDisplay2.offsetWidth / 2;
        const valueY = centerY + y - valueDisplay2.offsetHeight / 2;
        valueDisplay2.style.left = `${valueX}px`;
        valueDisplay2.style.top = `${valueY}px`;
    };

    const update = function (slider) {
        const value = slider.value;
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
    
    

    const renderSemicircularSlider = function () {
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
            value:0

        });
        const handleElement2 = $(sliderContainer).find(".rs-handle")[0];
        const sliderElement = $(sliderContainer).find(".rs-container")[0];
        const sliderTrackElement = sliderElement.querySelector(".rs-bg-color");
        handleElement2.setAttribute("class", handleElement2.getAttribute("class") + " smartlight");

        const smartlight_value = $(sliderContainer).find(".rs-tooltip")[0];
        smartlight_value.setAttribute("class", smartlight_value.getAttribute("class") + " smartlight_value");
        

        // Get the span element
        const spanElement = document.querySelector(".smartlight_value");
        const currentValue = parseFloat(spanElement.textContent);

    };

    renderSemicircularSlider();
// });

// Socket code...........
var socket;
var ip;

fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        console.log('ip : ', ip)
        socket = io.connect(ip)

        socket.on('connect', function () {
            console.log("connected");
        });
        socket.on('desklight_intensity', function (data) {
            updateLEDState(data.intensity, data.color);
        });
        var intensitySlider = document.getElementById('rangeInput');
        var textWrapper = document.querySelector('.smartlight_value');

        function updateLEDState(previousIntensity, previousColor) {
            console.log("previousIntensity",previousIntensity);
            console.log("previousColor",previousColor)
            const sliderElement = document.querySelector(".rs-container");
            const handleElement = sliderElement.querySelector(".rs-handle");
            const intensityPercentage = (previousIntensity / 255) * 100;
            sliderElement.style.setProperty("--handle-position", intensityPercentage + "%");
            $(sliderContainer).roundSlider("option", "value", intensityPercentage);
        
            // Update the text displayed by the slider handle
            const sliderHandle = $(".smartlight_value");
            if (sliderHandle.length > 0) {
                sliderHandle.text(intensityPercentage);
            }

            textWrapper.textContent = Math.round(intensityPercentage); 
            intensitySlider.value = Math.round(intensityPercentage);

            document.getElementById('brightness').textContent = previousColor;
            var slider = document.getElementById('brightness');
            const lampIcon = document.getElementById('lampIcon');
            if (previousColor === '1') {
                lampIcon.src = '../static/img/white_light_copy.png';
                slider.value = 16; 
            } else if (previousColor === '3') {
                lampIcon.src = '../static/img/light_led_copy.png';
                slider.value = 50; 
            } else if (previousColor === '2') {
                lampIcon.src = '../static/img/dark_led_copy.png';
                slider.value = 83; 
            }
        }
    })
});
