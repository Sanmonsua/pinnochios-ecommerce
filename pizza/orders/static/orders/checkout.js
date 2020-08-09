document.addEventListener('DOMContentLoaded', ()=>{
  var stripe = Stripe('pk_test_51HE29lKcPIFcZJbWFcKKqBmpys8ivpxmkN8iUoWm3gMESnX4RgRCZlt6TdAbIyxnKhwRKy0fQ50gS6TfGM5rOaVT008vR7AutP');
  var elements = stripe.elements();

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

  var card = elements.create("card", { style: style });
  card.mount("#card-element");
})
