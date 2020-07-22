import {Cart} from './cart.js';
const cart = new Cart()
const updateBtns = Array.from(document.getElementsByClassName('update-cart'));


updateBtns.map(elem => elem.addEventListener('click', async function () {
    await cart.updateItem(this.dataset.sku, this.dataset.action)
    let data = await cart.getItems()
    console.log(data)
}))

async function updateCartInNavBar() {
    let cartTotalElem = document.getElementById('cart-total-items');
    const url = `${location.protocol}//${location.host}/api/cart/quantity_of_items/`;
        let csrfToken = (window.user==="AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value:
        getCookie('csrftoken');
    const response = await fetch(url, {
        method:'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrfToken,
        },
    })
    let data = await response.json()
    cartTotalElem.innerHTML = data['total_quantity']

}

