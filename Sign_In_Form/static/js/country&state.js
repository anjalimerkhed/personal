var countryStateInfo = {
    India: {
        states: ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli"]
    },
    US: {
        states: ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia"]
    },
    Germany: {
        states: ["Baden-Wuerttemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen"]
    },
    Bangladesh: {
        states: ["Barisal", "Chittagong", "Dhaka", "Khulna", "Rajshahi", "Sylhet"]
    },
    Canada: {
        states: ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Nunavut"]
    },
    Denmark: {
        states: ["Arhus", "Bornholm", "Frederiksberg", "Frederiksborg", "Fyn", "Kobenhavn", "Kobenhavns", "Nordjylland", "Ribe", "Ringkobing", "Roskilde"]
    },
    Egypt: {
        states: ["Ad Daqahliyah", "Al Bahr al Ahmar", "Al Buhayrah", "Al Fayyum", "Al Gharbiyah", "Al Iskandariyah", "Al Isma'iliyah", "Al Jizah", "Al Minufiyah"]
    },
    Nepal: {
        states: ["Bagmati", "Bheri", "Dhawalagiri", "Gandaki", "Janakpur", "Karnali", "Kosi", "Lumbini", "Mahakali", "Mechi", "Narayani"]
    },
    NewZealand: {
        states: ["Auckland", "Bay of Plenty", "Canterbury", "Chatham Islands", "Gisborne", "Hawke's Bay", "Manawatu-Wanganui", "Marlborough"]
    },
    Pakistan: {
        states: ["Balochistan", "North-West Frontier Province", "Punjab", "Sindh", "Islamabad Capital Territory", "Federally Administered Tribal Areas"]
    },
};
window.onload = function () {
    const countrySelection = document.querySelector("#country_name"),
        stateSelection = document.querySelector("#state_name");
}
stateSelection.disabled = true;
for (let country in countryStateInfo) {
    countrySelection.options[countrySelection.options.length] = new Option(
        country,
        country
    );
}
//Todo: Country Changed

countrySelection.onchange = (e) => {
    stateSelection.disabled = false;
    // todo: Clear all options from State Selection
    stateSelection.length = 1; // remove all options bar first

    // if (e.target.selectedIndex < 1) return; // done

    // todo: Load states by looping over countryStateInfo
    for (let state in countryStateInfo[e.target.value]) {
        stateSelection.options[stateSelection.options.length] = new Option(
            state,
            state
        );
    }
};
