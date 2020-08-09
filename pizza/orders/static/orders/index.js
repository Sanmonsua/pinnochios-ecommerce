const toppingTemplate = Handlebars.compile(document.querySelector('#topping').innerHTML);
const addonTemplate = Handlebars.compile(document.querySelector('#addon').innerHTML);
const cartItemTemplate = Handlebars.compile(document.querySelector('#cart-item').innerHTML);

document.addEventListener('DOMContentLoaded', ()=>{

  load_cart();

  document.querySelectorAll(".product").forEach(p =>{
    p.onclick = () =>{
      get_product(p.dataset.product);
    }
  });

  document.querySelector('#addToCartButton').onclick = addToCart;
});


function get_product(product_id){
  const request = new XMLHttpRequest();
  request.open("GET", `products/${product_id}`);

  request.onload = () => {
    const data = JSON.parse(request.responseText);
    console.log(data);
    document.querySelector('#product-image').setAttribute('src', data.image_url)
    document.querySelector("#product-info").setAttribute('data-id', data.id)
    document.querySelector("#product-name").innerHTML = data.name + " - " + data.category;
    document.querySelector("#product-description").innerHTML = data.description;
    document.querySelector("#product-small-price-label").innerHTML = "Small $" + data.smallPrice;
    document.querySelector("#product-small-price-radio").value = data.smallPrice;
    document.querySelector("#product-large-price-label").innerHTML = "Large $" + data.largePrice;
    document.querySelector("#product-large-price-radio").value = data.largePrice;
    let toppingsSection = document.querySelector('#toppings');
    toppingsSection.innerHTML = "";
    if (data.toppings.length > 0){
      document.querySelector("#toppings-section").style.display = "block";
      data.toppings.forEach(t =>{
        const topping = toppingTemplate({"id":t.id, "name":t.name});
        toppingsSection.innerHTML += topping;
      });
    } else {
      document.querySelector("#toppings-section").style.display = "none";
    }
    let addonsSection = document.querySelector('#addons');
    addonsSection.innerHTML = "";
    if (data.addons.length > 0){
      document.querySelector("#addons-section").style.display = "block";
      data.addons.forEach(a =>{
        const addon = addonTemplate({"id":a.id, "name":a.name, "price":a.price});
        addonsSection.innerHTML += addon;
      });
    } else {
      document.querySelector("#addons-section").style.display = "none";
    }

  }

  request.send();
}

function load_cart() {
  const request = new XMLHttpRequest();
  request.open('GET', 'cart')

  request.onload = () =>{
    const data = JSON.parse(request.responseText);
    const cart = data.cart;
    document.querySelector('#cart-count').innerHTML = cart.length;
    document.querySelector('#cart-items-list').innerHTML = "";
    var total_price = 0;
    if (cart.length > 0){
      document.querySelector('#cart-empty-label').setAttribute("hidden", "true");
      document.querySelector('#clear-cart').removeAttribute("disabled");
      document.querySelector('#checkout').removeAttribute("disabled");
      cart.forEach( item =>{
        total_price += item.price;
        const item_content = cartItemTemplate(item);
        document.querySelector('#cart-items-list').innerHTML += item_content;
      })
    } else {
      document.querySelector('#cart-empty-label').removeAttribute("hidden");
      document.querySelector('#clear-cart').disabled = "true";
      document.querySelector('#checkout').disabled = "true";
    }

    document.querySelector('#checkout').innerHTML = `Checkout $ ${total_price}`;

  }


  request.send()
}


function closeAllModals() {

    const modals = document.getElementsByClassName('modal');

    for(let i=0; i<modals.length; i++) {
      modals[i].classList.remove('show');
      modals[i].setAttribute('aria-hidden', 'true');
      modals[i].setAttribute('style', 'display: none');
    }

    const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

    for(let i=0; i<modalsBackdrops.length; i++) {
      document.body.removeChild(modalsBackdrops[i]);
    }
}


function addToCart(){
  const request = new XMLHttpRequest();
  request.open('POST', 'addtocart')

  request.onload = () =>{
      load_cart();
      closeAllModals();
  }

  const data = new FormData();
  let price = 0;
  const product_id = document.querySelector('#product-info').dataset.id;
  data.append('product_id', product_id);

  const quantity = 1;
  data.append('quantity', quantity);

  let toppings = [];
  document.querySelectorAll('.topping').forEach( t =>{
    if (t.checked){
      toppings.push(t.id);
    }
  });
  data.append('toppings', toppings);

  let addons = [];
  document.querySelectorAll('.addon').forEach( a =>{
    if (a.checked){
      addons.push(a.id)
      price += parseFloat(a.dataset.price);
    }

  });
  data.append('addons', addons);

  document.querySelectorAll('.size-radio').forEach( s =>{
    if (s.checked){
      price += parseFloat(s.value);
    }
  });
  data.append('price', price);
  csrfmiddlewaretoken = document.querySelector("#addtocart-form input[name='csrfmiddlewaretoken']").value;
  data.append('csrfmiddlewaretoken', window.CSRF_TOKEN);

  request.send(data);
  return false;
}
