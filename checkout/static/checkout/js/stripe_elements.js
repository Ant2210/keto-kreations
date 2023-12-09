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
