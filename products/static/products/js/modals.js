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
                modal.hide();
            });
        } else if (variantCheckbox.checked) {
            const modal = new bootstrap.Modal(checkVariantModal);
            modal.show();
            // When undo-check-variants button is clicked, uncheck the variant checkbox and hide the modal
            document.getElementById('undo-check-variants').addEventListener('click', () => {
                variantCheckbox.checked = false;
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
                modal.hide();
            });
        } else if (onSaleCheckbox.checked) {
            const modal = new bootstrap.Modal(checkOnSaleModal);
            modal.show();
            // When undo-check-on-sale button is clicked, uncheck the on_sale checkbox and hide the modal
            document.getElementById('undo-check-on-sale').addEventListener('click', () => {
                onSaleCheckbox.checked = false;
                modal.hide();
            });
        }
    });
});