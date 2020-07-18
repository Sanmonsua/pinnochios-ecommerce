document.addEventListener('DOMContentLoaded', ()=>{
  
});


function get_product(product_id){
  const request = new XMLHttpRequest();
  request.open("GET", `products/${product_id}`);

  request.onload = () => {
    const data = JSON.parse(request.responseText);
    console.log(data);
  }

  request.send();
}
