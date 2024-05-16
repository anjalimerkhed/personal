// code of desklight.............
document.addEventListener('DOMContentLoaded', function() {
    const lightCheckbox = document.getElementById('lightCheckbox');
    lightCheckbox.addEventListener('change', function() {
        const isChecked = this.checked;
        const url = isChecked ? '/turnon/api/' : '/turnoff/api/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    });
});



fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)
        // Event listener for receiving LED state updates
        socket.on('desklight', function(data) {
        console.log('lightCheckbox:', data.value);
        const lightCheckbox = document.getElementById('lightCheckbox');
        lightCheckbox.checked = (data.value !== '0');
    });
    })



// code for Autobrightness...
document.addEventListener('DOMContentLoaded', function() {
    const Autobrightness = document.getElementById('Autobrightness');
    Autobrightness.addEventListener('change', function() {
        const isChecked = this.checked;
        const url = isChecked ? '/autobrightnessEnable/api/' : '/autobrightnessDisable/api/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    });
});

fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)
        // Event listener for receiving LED state updates
        socket.on('split_desklight', function(data) {
            console.log("data.......", data)
            const elementArray = data.split_desklight;
            const fifthElement = elementArray[4];
            const splitElement = fifthElement.split(":");
            console.log("fifthElement......", splitElement);
            const Autobrightness = document.getElementById('Autobrightness');
            Autobrightness.checked = (fifthElement !== '0');
        });
    })






// code for diffuser.........
document.addEventListener('DOMContentLoaded', function() {
    const diffuser = document.getElementById('diffuser');
    diffuser.addEventListener('change', function() {
        const isChecked = this.checked;
        const url = isChecked ? '/diffuseron/api/' : '/diffuseroff/api/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    });
});



// socket

fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)
        // Event listener for receiving LED state updates
        socket.on('diffuser', function(data) {
            console.log('diffuser_status:', data.value);
            const diffuser = document.getElementById('diffuser');
            diffuser.checked = (data.value !== '0');
        });
    })



// diffuser continousONOFF
document.addEventListener('DOMContentLoaded', function() {
    const diffuserAuto = document.getElementById('diffuserAuto');
    diffuserAuto.addEventListener('change', function() {
        const isChecked = this.checked;
        const url = isChecked ? '/DiffuserEnable/api/' : '/DiffuserDisable/api/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    });
});

// Code for autoONOFF............



fetch("../static/js/ip.json")
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        ip = data.ip
        socket = io.connect(ip)
        socket.on('split_diffuser', function(data) {
            console.log("data.......", data);
            const elementArrayDiffuser = data.split_diffuser;
            console.log("elementArrayDiffuser", elementArrayDiffuser);
            const desiredValue = elementArrayDiffuser[6] + ':' + elementArrayDiffuser[6];
            console.log("desiredValue:", desiredValue);
            const diffuserAuto = document.getElementById('diffuserAuto');
            diffuserAuto.checked = (desiredValue !== '0:0');
           
        });
    })