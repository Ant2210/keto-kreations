const variantCheckbox = document.getElementById('id_has_variants');
const onSaleCheckbox = document.getElementById('id_on_sale');
const priceDiv = document.getElementById('div_id_price');
const priceInput = document.getElementById('id_price');
const salePriceDiv = document.getElementById('div_id_sale_price');
const salePriceInput = document.getElementById('id_sale_price');
const sizeDiv = document.getElementById('div_id_size');
const sizeInput = document.getElementById('id_size');
const sizeUnitDiv = document.getElementById('div_id_size_unit');
const sizeUnitInput = document.getElementById('id_size_unit');
const stockCountDiv = document.getElementById('div_id_stock_count');

/*
Functions to toggle the visibility and required attributes of the relevant 
fields depending on whether the product has variants or is on sale
*/

// Function to toggle the d-none class on the price, sale price, size, size 
//unit and stock count fields when the product has variants
const toggleVisibility = () => {
    priceDiv.classList.toggle('d-none', variantCheckbox.checked);
    sizeDiv.classList.toggle('d-none', variantCheckbox.checked);
    sizeUnitDiv.classList.toggle('d-none', variantCheckbox.checked);
    stockCountDiv.classList.toggle('d-none', variantCheckbox.checked);
};

// Function to toggle the required attribute on the price, size and size unit
// fields when the product does not have variants
const toggleRequired = () => {
    priceInput.required = !variantCheckbox.checked;
    sizeInput.required = !variantCheckbox.checked;
    sizeUnitInput.required = !variantCheckbox.checked;
    document.querySelector('label[for="id_price"]').innerHTML = 'Price*';
    document.querySelector('label[for="id_size"]').innerHTML = 'Size*';
    document.querySelector('label[for="id_size_unit"]').innerHTML = 'Size unit*';
    toggleSalePriceRequired();
    toggleSalePriceVisibility();
};

// Add event listener to checkbox
variantCheckbox.addEventListener('change', () => {
        toggleVisibility();
        toggleRequired();
});

// Function to toggle the class d-none on the sale price field when the
//on_sale checkbox is checked
const toggleSalePriceVisibility = () => {
    if (onSaleCheckbox.checked && !variantCheckbox.checked) {
        salePriceDiv.classList.remove('d-none');
    } else {
        salePriceDiv.classList.add('d-none');
    }
};

// Function to toggle the required attribute on the sale price field when
// the on_sale checkbox is checked
const toggleSalePriceRequired = () => {
    if (onSaleCheckbox.checked && !variantCheckbox.checked) {
        salePriceInput.required = true;
        document.querySelector('label[for="id_sale_price"]').innerHTML = 'Sale price*';
    } else {
        salePriceInput.required = false;
    }
};

// Add event listener to on_sale checkbox
onSaleCheckbox.addEventListener('change', () => {
    toggleSalePriceVisibility();
    toggleSalePriceRequired();
});

// Initial execution to set the initial state
toggleSalePriceVisibility();
toggleSalePriceRequired();
toggleVisibility();
toggleRequired();

/* 
Warning Modals for when the user tries to check or uncheck the variant or 
on sale checkboxes
*/

// Product Variant Modals
document.addEventListener('DOMContentLoaded', () => {
    const variantCheckbox = document.getElementById('id_has_variants');
    const uncheckVariantModal = document.getElementById('uncheck-variants-modal');
    const checkVariantModal = document.getElementById('check-variants-modal');

    // When variant checkbox is unchecked, show bootstrap uncheck-variants-modal
    // and if it is checked show the check-variants-modal
    variantCheckbox.addEventListener('change', () => {
        if (!variantCheckbox.checked) {
            const modal = new bootstrap.Modal(uncheckVariantModal);
            modal.show();
            // When undo-uncheck-variants button is clicked, re-check the variant checkbox and hide the modal
            document.getElementById('undo-uncheck-variants').addEventListener('click', () => {
                variantCheckbox.checked = true;
                toggleRequired();
                toggleVisibility();
                modal.hide();
            });
        } else if (variantCheckbox.checked) {
            const modal = new bootstrap.Modal(checkVariantModal);
            modal.show();
            // When undo-check-variants button is clicked, uncheck the variant checkbox and hide the modal
            document.getElementById('undo-check-variants').addEventListener('click', () => {
                variantCheckbox.checked = false;
                toggleRequired();
                toggleVisibility();
                modal.hide();
            });
        }
    });
});

// On Sale Modals
document.addEventListener('DOMContentLoaded', () => {
    const onSaleCheckbox = document.getElementById('id_on_sale');
    const uncheckOnSaleModal = document.getElementById('uncheck-on-sale-modal');
    const checkOnSaleModal = document.getElementById('check-on-sale-modal');

    // When on_sale checkbox is unchecked, show bootstrap uncheck-on-sale-modal
    // and if it is checked show the check-on-sale-modal
    onSaleCheckbox.addEventListener('change', () => {
        if (!onSaleCheckbox.checked) {
            const modal = new bootstrap.Modal(uncheckOnSaleModal);
            modal.show();
            // When undo-uncheck-on-sale button is clicked, re-check the on_sale checkbox and hide the modal
            document.getElementById('undo-uncheck-on-sale').addEventListener('click', () => {
                onSaleCheckbox.checked = true;
                toggleSalePriceRequired();
                toggleSalePriceVisibility();
                modal.hide();
            });
        } else if (onSaleCheckbox.checked) {
            const modal = new bootstrap.Modal(checkOnSaleModal);
            modal.show();
            // When undo-check-on-sale button is clicked, uncheck the on_sale checkbox and hide the modal
            document.getElementById('undo-check-on-sale').addEventListener('click', () => {
                onSaleCheckbox.checked = false;
                toggleSalePriceRequired();
                toggleSalePriceVisibility();
                modal.hide();
            });
        }
    });
});