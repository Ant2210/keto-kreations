// Hide the price, sale price, size, size unit and stock count fields if the product has variants
// and make the price, size and size unit fields required if the product does not have variants
document.addEventListener('DOMContentLoaded', () => {
    const variantCheckbox = document.getElementById('id_has_variants');
    const priceDiv = document.getElementById('div_id_price');
    const priceInput = document.getElementById('id_price');
    const salePriceDiv = document.getElementById('div_id_sale_price');
    const sizeDiv = document.getElementById('div_id_size');
    const sizeInput = document.getElementById('id_size');
    const sizeUnitDiv = document.getElementById('div_id_size_unit');
    const sizeUnitInput = document.getElementById('id_size_unit');
    const stockCountDiv = document.getElementById('div_id_stock_count');

    // Function to toggle the class
    const toggleVisibility = () => {
        priceDiv.classList.toggle('d-none', variantCheckbox.checked);
        salePriceDiv.classList.toggle('d-none', variantCheckbox.checked);
        sizeDiv.classList.toggle('d-none', variantCheckbox.checked);
        sizeUnitDiv.classList.toggle('d-none', variantCheckbox.checked);
        stockCountDiv.classList.toggle('d-none', variantCheckbox.checked);
    };

    const toggleRequired = () => {
        priceInput.required = !variantCheckbox.checked;
        sizeInput.required = !variantCheckbox.checked;
        sizeUnitInput.required = !variantCheckbox.checked;
        document.querySelector('label[for="id_price"]').innerHTML = 'Price*';
        document.querySelector('label[for="id_size"]').innerHTML = 'Size*';
        document.querySelector('label[for="id_size_unit"]').innerHTML = 'Size unit*';
    }

    // Add event listener to checkbox
    variantCheckbox.addEventListener('change', () => {
         toggleVisibility();
         toggleRequired();
    });

    // Initial execution to set the initial state
    toggleVisibility();
    toggleRequired();
});

// Hide the sale price fields if on_sale is not checked
document.addEventListener('DOMContentLoaded', () => {
    const onSaleCheckbox = document.getElementById('id_on_sale');
    const salePriceDiv = document.getElementById('div_id_sale_price');

    // Function to toggle the class
    const toggleSalePriceVisibility = () => {
        salePriceDiv.classList.toggle('d-none', !onSaleCheckbox.checked);
    };

    // Add event listener to on_sale checkbox
    onSaleCheckbox.addEventListener('change', toggleSalePriceVisibility);

    // Initial execution to set the initial state
    toggleSalePriceVisibility();
});