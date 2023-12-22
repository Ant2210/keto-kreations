/* 
Load country list and set default country if there is one
*/
let countrySelect = document.getElementById('id_default_country');
let countrySelected = countrySelect.value;

if (!countrySelected) {
    countrySelect.style.color = 'rgba(33, 37, 41, 0.5)';
}

countrySelect.addEventListener('change', function () {
    countrySelected = this.value;

    if (!countrySelected) {
        this.style.color = 'rgba(33, 37, 41, 0.5)';
    } else {
        this.style.color = '#212529';
    }
});