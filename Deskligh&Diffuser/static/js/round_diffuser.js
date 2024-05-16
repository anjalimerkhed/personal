document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.getElementById("root");
    const rangeInput = document.getElementById("rangeInput");
    const valueDisplay = document.getElementById("valueDisplay");

    const updateValueDisplayPosition = function (value) {
        const sliderElement = document.querySelector(".rs-container");
        const radius = parseFloat(sliderElement.getAttribute("r"));
        const angle = (value * 380) / 100; // Convert percentage to angle
        const x = radius * Math.cos((angle * Math.PI) / 180);
        const y = radius * Math.sin((angle * Math.PI) / 180);
        const sliderRect = sliderElement.getBoundingClientRect();
        const centerX = sliderRect.left + sliderRect.width / 2;
        const centerY = sliderRect.top + sliderRect.height / 2;
        // const valueX = centerX + x - valueDisplay.offsetWidth / 2;
        // const valueY = centerY + y - valueDisplay.offsetHeight / 2;
        // valueDisplay.style.left = `${valueX}px`;
        // valueDisplay.style.top = `${valueY}px`;
    };

    const update = function (e) {
        const value = e.value;
        let time = "";
        switch (value) {
            case 1:
                time = "1 min";
                break;
            case 2:
                time = "5 min";
                break;
            case 3:
                time = "10 min";
                break;
            case 4:
                time = "15 min";
                break;
            default:
                time = "";
                break;
        }
        valueDisplay.innerText = time;
        updateValueDisplayPosition(value);
    };
    
    

    const renderSemicircularSlider = function () {
        $(sliderContainer).roundSlider({
            radius: 100,
            width: 8,
            handleSize: "+20",
            startAngle: 0,
            endAngle: 380,
            sliderType: "min-range",
            svgMode: true,
            change: update,
            drag: update,
            pathColor: "#a5a5a5",
            circleShape: "half-right",
            value: 1, // Set initial value to 1
            min: 1, // Set minimum value to 1
            max: 4, // Set maximum value to 4
            step: 1, // Set step to 1
            tooltipFormat: function (args) {
                // Customize tooltip format
                const values = ["1 min", "5 min", "10 min", "15 min"];
                return values[args.value - 1];
            }
        });
    
        // Set specific labels for each step
        const steps = [1, 2, 3, 4];
        for (let i = 0; i < steps.length; i++) {
            $(sliderContainer).roundSlider("option", "rangeValue", [1, steps[i]]);
        }
    };
    
    renderSemicircularSlider();
    
    
});
