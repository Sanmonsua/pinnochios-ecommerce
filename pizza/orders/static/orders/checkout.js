document.addEventListener('DOMContentLoaded', () => {
  var stripe = Stripe('pk_test_51HE29lKcPIFcZJbWFcKKqBmpys8ivpxmkN8iUoWm3gMESnX4RgRCZlt6TdAbIyxnKhwRKy0fQ50gS6TfGM5rOaVT008vR7AutP');

  const request = new XMLHttpRequest();
  request.open('GET', 'charge');

  var clientSecret;
  request.onload =()=>{
    console.log(request.responseText);
    const data = JSON.parse(request.responseText);
    clientSecret = data.clientSecret;
  }

  request.send()

  var elements = stripe.elements();

  document.querySelector('#submit').disabled = true;

  var style = {
    base: {
      color: '#303238',
      fontSize: '20px',
      fontFamily: '"Open Sans", sans-serif',
      fontSmoothing: 'antialiased',
      '::placeholder': {
        color: '#6c757d',
      },
    },
    invalid: {
      color: '#e5424d',
      ':focus': {
        color: '#303238',
      },
    },
  };

  var card = elements.create("card", {
    style: style
  });
  card.mount("#card-element");
  card.on("change", function(event) {
    // Disable the Pay button if there are no card details in the Element
    document.querySelector("button").disabled = event.empty;
    document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
  });
  var form = document.getElementById("payment-form");
  form.addEventListener("submit", function(event) {
    event.preventDefault();
    // Complete payment when the submit button is clicked
    payWithCard(stripe, card, clientSecret);
  });
})

var payWithCard = function(stripe, card, clientSecret) {
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function(result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message);
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id);
      }
    });
};

/* ------- UI helpers ------- */
// Shows a success message when the payment is complete
var orderComplete = function(paymentIntentId) {
  loading(false);
  const request = new XMLHttpRequest();
  request.open('POST', 'checkout')

  request.onload = () =>{
    window.location.replace("/your-orders");
  }

  const data = new FormData();
  data.append('paymentIntentId', paymentIntentId);
  data.append('csrfmiddlewaretoken', window.CSRF_TOKEN);
  request.send(data);
};
// Show the customer the error from Stripe if their card fails to charge
var showError = function(errorMsgText) {
  loading(false);
  alert(errorMsgText);
};
// Show a spinner on payment submission
var loading = function(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};
