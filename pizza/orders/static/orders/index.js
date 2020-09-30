const toppingTemplate = Handlebars.compile(
	document.querySelector('#topping').innerHTML
)
const addonTemplate = Handlebars.compile(
	document.querySelector('#addon').innerHTML
)
const cartItemTemplate = Handlebars.compile(
	document.querySelector('#cart-item').innerHTML
)

document.addEventListener('DOMContentLoaded', function onDocumentLoaded() {
	loadCart()

	document.querySelectorAll('.product').forEach(setProductOnClick)
	document.querySelector('#addToCartButton').onclick = addToCart

	function setProductOnClick(product) {
		product.onclick = function productOnClick() {
			getProduct(product.dataset.product)
		}
	}
})

function getProduct(productId) {
	var request = new XMLHttpRequest()
	request.open('GET', `products/${productId}`)

	request.onload = function onGetProductRequestLoad() {
		var {
			image_url,
			id,
			name,
			category,
			description,
			smallPrice,
			largePrice,
			toppings,
			addons,
			max_toppings,
		} = JSON.parse(request.responseText)
		document.querySelector('#product-image').setAttribute('src', image_url)
		document.querySelector('#product-info').setAttribute('data-id', id)
		document.querySelector(
			'#product-name'
		).innerHTML = `${name} - ${category}`
		document.querySelector('#product-description').innerHTML = description
		document.querySelector(
			'#product-small-price-label'
		).innerHTML = `Small $${smallPrice}`
		document.querySelector('#product-small-price-radio').value = smallPrice
		document.querySelector(
			'#product-large-price-label'
		).innerHTML = `Large $${largePrice}`
		document.querySelector('#product-large-price-radio').value = largePrice

		createToppingsSection()
		createAddOnsSection()
		createCheckboxes()

		// ---------------------------------------------------

		function createToppingsSection() {
			var toppingsSection = document.querySelector('#toppings')
			toppingsSection.innerHTML = ''
			if (toppings.length > 0) {
				document.querySelector('#toppings-section').style.display =
					'block'
				toppings.forEach(createToppingElement)
			} else {
				document.querySelector('#toppings-section').style.display =
					'none'
			}

			function createToppingElement({ id, name }) {
				var toppingElement = toppingTemplate({ id, name })
				toppingsSection.innerHTML += toppingElement
			}
		}

		function createAddOnsSection() {
			var addonsSection = document.querySelector('#addons')
			addonsSection.innerHTML = ''
			if (addons.length > 0) {
				document.querySelector('#addons-section').style.display =
					'block'
				addons.forEach(createAddOnElement)
			} else {
				document.querySelector('#addons-section').style.display = 'none'
			}

			function createAddOnElement({ id, name, price }) {
				var addOn = addonTemplate(id, name, price)
				addonsSection.innerHTML += addOn
			}
		}

		function createCheckboxes() {
			document
				.querySelectorAll("input[name='groupOfCheckboxes']")
				.forEach(createToppingsCheckbox)

			function createToppingsCheckbox(checkbox) {
				checkbox.addEventListener('change', selectToppingCheckbox)
			}
			function selectToppingCheckbox() {
				if (
					document.querySelectorAll(
						"input[name='groupOfCheckboxes']:checked"
					).length > max_toppings
				) {
					checkbox.checked = false
				}
			}
		}
	}

	request.send()
}

function loadCart() {
	var request = new XMLHttpRequest()
	request.open('GET', 'cart')

	request.onload = function onLoadCartRequest() {
		var { cart } = JSON.parse(request.responseText)
		document.querySelector('#cart-count').innerHTML = cart.length
		document.querySelector('#cart-items-list').innerHTML = ''
		var totalPrice = 0
		if (cart.length > 0) {
			document
				.querySelector('#cart-empty-label')
				.setAttribute('hidden', 'true')
			document.querySelector('#clear-cart').removeAttribute('disabled')
			document.querySelector('#checkout').removeAttribute('disabled')
			cart.forEach(loadItem)
		} else {
			document
				.querySelector('#cart-empty-label')
				.removeAttribute('hidden')
			document.querySelector('#clear-cart').disabled = 'true'
			document.querySelector('#checkout').disabled = 'true'
		}

		function loadItem(item) {
			totalPrice += item.price
			var itemElement = cartItemTemplate(item)
			document.querySelector('#cart-items-list').innerHTML += itemElement
		}

		document.querySelector(
			'#checkout'
		).innerHTML = `Checkout $ ${totalPrice}`
	}

	request.send()
}

function closeAllModals() {
	var modals = document.getElementsByClassName('modal')
	modals.forEach(closeModal)

	var modalsBackdrops = document.getElementsByClassName('modal-backdrop')
	modalsBackdrops.forEach(modalBackdropRemove)

	function closeModal(modal) {
		modal.classList.remove('show')
		modal.setAttribute('aria-hidden', 'true')
		modal.setAttribute('style', 'display: none')
	}

	function modalBackdropRemove(modalBackdrop) {
		document.body.removeChild(modalBackdrop)
	}
}

function addToCart() {
	var request = new XMLHttpRequest()
	request.open('POST', 'addtocart')

	request.onload = function onAddToCartRequest() {
		loadCart()
		closeAllModals()
	}

	var data = new FormData()
	var price = 0

	var productId = document.querySelector('#product-info').dataset.id
	data.append('product_id', productId)

	var quantity = 1
	data.append('quantity', quantity)

	var toppings = []
	document.querySelectorAll('.topping').forEach(addTopping)
	data.append('toppings', toppings)

	var addons = []
	document.querySelectorAll('.addon').forEach(addAddon)
	data.append('addons', addons)

	document.querySelectorAll('.size-radio').forEach(applySizeToPrice)

	data.append('price', price)
	data.append('csrfmiddlewaretoken', window.CSRF_TOKEN)

	request.send(data)
	return false

	// -------------------------------------------------------------

	function addTopping(topping) {
		var { id, checked } = topping
		if (checked) {
			toppings.push(id)
		}
	}

	function addAddon(addOn) {
		var { checked, id } = addOn
		if (checked) {
			addons.push(id)
			price += Number(addOn.dataset.price)
		}
	}

	function applySizeToPrice(sizeOption) {
		var { checked, value } = sizeOption
		if (checked) {
			price += Number(value)
		}
	}
}
