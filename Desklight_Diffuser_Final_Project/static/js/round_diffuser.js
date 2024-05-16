document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.getElementById("root");
    const rangeInput = document.getElementById("rangeInput");
    const valueDisplay = document.getElementById("valueDisplay");

    const updateValueDisplayPosition = function (value) {
        const sliderElement = document.querySelector(".rs-container");
        const radius = parseFloat(sliderElement.getAttribute("r"));
        // const angle = (value * 20) / 20; // Convert percentage to angle
        const x = radius * Math.cos((angle * Math.PI) / 180);
        const y = radius * Math.sin((angle * Math.PI) / 180);
        const sliderRect = sliderElement.getBoundingClientRect();
        const centerX = sliderRect.left + sliderRect.width / 2;
        const centerY = sliderRect.top + sliderRect.height / 2;
        const valueX = centerX + x - valueDisplay.offsetWidth / 2;
        const valueY = centerY + y - valueDisplay.offsetHeight / 2;
        valueDisplay.style.left = `${valueX}px`;
        valueDisplay.style.top = `${valueY}px`;
    };

// code by nikky 
const update = function (e) {
    const value = e.value;
    let displayValue;

    const labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "20"];

    for (let i = 0; i < labels.length; i++) {
        if (value <= parseInt(labels[i])) {
            displayValue = labels[i];
            break;
        }
    }

    const airdiffuserValueElement = document.querySelector(".airdiffuser_value");
    if (airdiffuserValueElement) {
        airdiffuserValueElement.innerText = displayValue;
    }

    const validValues = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "20"];
    if (validValues.includes(displayValue)) {
        publishValue(displayValue);
    }

    updateValueDisplayPosition(value);
};

    
    const publishValue = function(value) {
        const data = {
            'ContinuousONOFF': `${value}:${value}`
        };
    
        fetch('/ContinuousONOFF', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('ContinuousONOFF published successfully');
        })
        .catch(error => {
            console.error('Error publishing ContinuousONOFF:', error);
        });
    };
    



    const renderSemicircularSlider = function () {
        $(sliderContainer).roundSlider({
            radius: 100,
            width: 8,
            handleSize: "+20",
            min:0,
            max:20,
            startAngle: 0,
            endAngle: 180,
            sliderType: "min-range",
            svgMode: true,
            change: update,
            drag: update,
            pathColor: "#a5a5a5",
            circleShape: "half-right",
            value:0,
            change: function (args) {
                var sliderValue = args.value;
                sendDataToBackend(sliderValue);
            }

        });
        const handleElement = $(sliderContainer).find(".rs-handle")[0];

        const sliderElement = $(sliderContainer).find(".rs-container")[0];

        const sliderTrackElement = sliderElement.querySelector(".rs-bg-color");
        handleElement.setAttribute("class", handleElement.getAttribute("class") + " diffuser_handle");

        const airdiffuser_value = $(sliderContainer).find(".rs-tooltip")[0];
        airdiffuser_value.setAttribute("class", airdiffuser_value.getAttribute("class") + " airdiffuser_value");

    };

    renderSemicircularSlider();

// Socket code...........
fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)
        socket.on('connect', function () {
        });
        socket.on('split_diffuser', function(data) {
            console.log("data.......", data);
            const elementArrayDiffuser = data.split_diffuser;
            console.log("elementArrayDiffuser", elementArrayDiffuser);
            const desiredValue = parseFloat(elementArrayDiffuser[6]); 
            console.log("desiredValue:......", desiredValue);
            $(sliderContainer).roundSlider("option", "value", desiredValue);
            const sliderHandle = $(".airdiffuser_value");
            if (sliderHandle.length > 0) {
                sliderHandle.text(desiredValue);
            }
        });
    })

});
