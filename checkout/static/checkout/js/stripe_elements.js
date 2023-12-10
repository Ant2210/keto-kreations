/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

const stripePublicKey = document.querySelector('#id_stripe_public_key').textContent.slice(1, -1);
const clientSecret = document.querySelector('#id_client_secret').textContent.slice(1, -1);
const stripe = Stripe(stripePublicKey);
// Customer font info found here: https://stackoverflow.com/questions/61324672/custom-font-is-not-loaded-in-stripe-element
const elements = stripe.elements({
    fonts: [
        {
            cssSrc: 'https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap',
        },
    ],
});
const style = {
    base: {
        fontFamily: '"Roboto Condensed", sans-serif',
        fontSize: '16px',
        color: '#212529',
        '::placeholder': {
            color: 'rgba(33, 37, 41, 0.5)',
            fontSize: '16px',   

        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
const card = elements.create('card', {style: style});
card.mount('#card-element');

document.querySelector('#card-element').classList.add('form-control');


// Handle realtime validation errors on the card element
card.addEventListener('change', (event) => {
    const errorDiv = document.getElementById('card-errors');
    
    if (event.error) {
        const html = `
            <span class="icon" role="alert">
                <i class="fas fa-times text-danger"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = html;
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
const form = document.getElementById('payment-form');
const loadingOverlay = document.getElementById('loading-overlay');
const errorDiv = document.getElementById('card-errors');
const submitButton = document.getElementById('submit-button');

form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    card.update({ disabled: true });
    submitButton.disabled = true;
    loadingOverlay.classList.remove('d-none');

    const saveInfo = Boolean(document.getElementById('id-save-info').checked);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    const url = '/checkout/cache_checkout_data/';



    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData),
        });

        if (!response.ok) {
            let html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>'There was an error processing your request. Please\
                     try again.'</span>`;
            errorDiv.innerHTML = html;
            loadingOverlay.classList.add('d-none');
            card.update({ disabled: false });
            submitButton.disabled = false;
        }


        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.full_name.value.trim(),
                    phone: form.phone_number.value.trim(),
                    email: form.email.value.trim(),
                    address: {
                        line1: form.street_address1.value.trim(),
                        line2: form.street_address2.value.trim(),
                        city: form.town_or_city.value.trim(),
                        country: form.country.value.trim(),
                        state: form.county.value.trim(),
                    }
                }
            },
            shipping: {
                name: form.full_name.value.trim(),
                phone: form.phone_number.value.trim(),
                address: {
                    line1: form.street_address1.value.trim(),
                    line2: form.street_address2.value.trim(),
                    city: form.town_or_city.value.trim(),
                    country: form.country.value.trim(),
                    postal_code: form.postcode.value.trim(),
                    state: form.county.value.trim(),
                }
            },
        });

        if (result.error) {
            let html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
            errorDiv.innerHTML = html;
            loadingOverlay.classList.add('d-none');
            card.update({ disabled: false });
            submitButton.disabled = false;
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle the error as needed
        location.reload();
    }
});