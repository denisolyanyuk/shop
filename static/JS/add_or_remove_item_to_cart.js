
const updateBtns = Array.from(document.getElementsByClassName('update-cart'));


updateBtns.map(elem => elem.addEventListener('click', async function () {

    const sku = this.dataset.sku;
    const action = this.dataset.action;
    await updateItem(sku, action)
    await updateCartInNavBar()
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

async function updateItem(sku, action) {
    const url = `${location.protocol}//${location.host}/api/cart/${action}/`;
    let csrfToken = (window.user==="AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value:
        getCookie('csrftoken');

    const response = await fetch(url, {
        method:'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrfToken,
        },
        body: JSON.stringify({
            'sku': sku,
        }),
    })
    await response

}