function updateCurrentDate() {
    const currentDate = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = currentDate.toLocaleDateString(undefined, options);
    document.getElementById("currentDateSpan").textContent = formattedDate;
}
updateCurrentDate();

function updateCurrentTime() {
    const currentDate = new Date();
    const hours = currentDate.getHours();
    const minutes = currentDate.getMinutes();
    const amPM = hours >= 12 ? 'PM' : 'AM';
    const formattedTime = `${(hours % 12 === 0 ? 12 : hours % 12)}:${minutes.toString().padStart(2, '0')} ${amPM}`;
    document.getElementById("currentTimeSpan").textContent = formattedTime;
}

updateCurrentTime();
setInterval(updateCurrentTime, 60000);


var ip

function ip_func() {
    fetch("../static/js/ip.json")
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log(data.ip);
            ip = data.ip + '/test';
        });
}
ip_func()


function display(data1) {

    if (data1) {
        
        if (data1.temp) {
            document.getElementById("temp").innerHTML = parseFloat(data1.temp).toFixed(1);
        }

        if (data1.hum) {
            document.getElementById("hum").innerHTML = parseFloat(data1.hum).toFixed(0);
        }

        if (data1.dp) {
            document.getElementById("dp").innerHTML = parseFloat(data1.dp).toFixed(0);
        }
    } else {
        console.error('No data received');
    }
    function updateBackgroundColor() {
        const container = document.getElementById('container');

        // Assuming data1 is an array of objects with a 'time' property
        data1.forEach((item, index) => {
            timestamp = new Date(item.time);
            // Adjust for the local timezone offset
            timestamp.setMinutes(timestamp.getMinutes() + timestamp.getTimezoneOffset());
            // Update the background color based on the condition
            const elementId = `container_${index + 1}`;
            const containerElement = document.getElementById(elementId);

            // Get the current datetime 
            currentTime = new Date();
    
            function diff_minutes(currentTime, timestamp) {

                var diff = (currentTime.getTime() - timestamp.getTime()) / 1000;
                diff /= 60;
                return Math.abs(Math.round(diff)) >= 30;

            }

            if (diff_minutes(currentTime, timestamp)) {
                containerElement.style.backgroundColor = 'grey';
            } else {
                containerElement.style.backgroundColor = '#EAF4FE';
            }
        });
    }
    updateBackgroundColor();
    setInterval(updateBackgroundColor, 60000);

}

async function send() {
    try {
        const response = await fetch(ip, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                display(data);
            } else {
                console.log('Response is not in JSON format');
            }
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

var s_data = setInterval(send, 5000);


function deleteDevice() {
    console.log("Delete Device clicked");
}

function addDevice() {
    console.log("Add Device clicked");
}