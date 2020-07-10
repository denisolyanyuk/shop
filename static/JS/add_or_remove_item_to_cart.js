
const updateBtns = Array.from(document.getElementsByClassName('update-cart'));
updateBtns.map(elem => elem.addEventListener('click', function () {

    const SKU = this.dataset.sku;
    const action = this.dataset.action;
    updateUserOrder(SKU, action)

}))


async function updateUserOrder(SKU, action) {
    const url = `${location.protocol}//${location.host}/update_item/`;
    let csrfToken = (window.user==="AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value:
        getCookie('csrftoken');

    const response = await fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrfToken,
        },
        body: JSON.stringify({
            'SKU': SKU,
            'action': action,
        }),
    })
    const data = await response.json()
    location.reload()
}