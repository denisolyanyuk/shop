export class Cart {
    baseUrl = `${location.protocol}//${location.host}/api/cart/`
    csrfToken = (window.user === "AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value :
        getCookie('csrftoken');


    async updateItem(sku, action) {
        await this._request('PATCH', action+'/', {'sku':sku})
    }

    async getItems(){
        let data = await this._request('GET')
        return data.json()
    }

    _request (method, url='', body='') {
        let params = {
            method:method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            }};
        if (body) {
            params['body'] = JSON.stringify(body);
        }

        return  fetch(this.baseUrl +url, params)

    }

}


export class PageWorker {
    #mediaDir = ''
    refreshCartItemsAmountInNavBar(amount){
        const cartTotalElem = document.getElementById('"cart-total-items"');
        cartTotalElem.innerHTML = amount
    }

    refreshCartItemsInCart(items){
        const container = document.getElementById('cart-rows-container')

        items.forEach((elem) => {


        })
    }

    _createCartItemRow(item) {
        let row = document.createElement('div')
        row.className = 'cart-row'
        let imageDiv = document.createElement('div')
        imageDiv.className = 'col-sm'
        let image = document.createElement('img')
        image.className = "row-image"
    <img class="row-image" src=" {{ item.product.main_image.url }}">

    }
}