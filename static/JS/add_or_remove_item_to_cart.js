
const updateBtns = Array.from(document.getElementsByClassName('update-cart'));
console.log(user)
updateBtns.map(elem => elem.addEventListener('click', function () {

    const SKU = this.dataset.sku;
    const action = this.dataset.action;
    if (user==="AnonymousUser") {
        console.log('Not logged in')
    } else {
        updateUserOrder(SKU, action)
    }


}))


async function updateUserOrder(SKU, action) {
    const url = `${location.protocol}//${location.host}/update_item/`;
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({
            'SKU': SKU,
            'action': action,
        }),
    })
    const data = await response.json()
    location.reload()
}