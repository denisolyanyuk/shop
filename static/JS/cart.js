export class Cart {
    baseUrl = `${location.protocol}//${location.host}/api/cart/`
    csrfToken = (window.user === "AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value :
        getCookie('csrftoken');

    constructor(elem) {
      this._elem = elem;
      elem.addEventListener('click', this.onClick.bind(this))
    }

    onClick(event) {
        let action = event.target.dataset.cartAction;
        if (action) {
            const sku = event.target.dataset.sku
            this[action](sku);
        }
    }

    async addItem(sku) {
        const response = await this._request('POST', 'add_item', {'sku':sku})
        const jsonResponse = await response.json()
        const cartInfo = jsonResponse['data']['cart']
        let cartItem = this._getCartItemBySku(sku,cartInfo)
        this._refreshCartItemRow(cartItem, sku)
        this._refreshCartInfo(cartInfo)
    }

    async removeItem(sku) {
        const response = await this._request('POST', 'remove_item', {'sku': sku})
        const jsonResponse = await response.json()
        const cartInfo = jsonResponse['data']['cart']
        let cartItem = this._getCartItemBySku(sku,cartInfo)
        this._refreshCartItemRow(cartItem, sku)
        this._refreshCartInfo(cartInfo)
    }

    _refreshCartItemRow(cartItem, sku) {
        const row = document.querySelector(`div[class*="cart-row"][data-sku="${sku}"]`)
        if (row) {
            if (cartItem) {
                row.querySelector('div[class*="quantity-column"]>p').textContent  = cartItem['quantity']
                row.querySelector('div[class*="item-price-column"]>[class="item-price"]').textContent  = cartItem['cart_item_price']
            } else {
                row.remove()
            }
        }

    }

    _refreshCartInfo(cartInfo) {
        document.querySelectorAll('[class*=total-quantity-of-items]').forEach(elem=> elem.textContent = cartInfo['quantity_of_items'])
        document.querySelectorAll('[class*=total-price]').forEach(elem=> elem.textContent = cartInfo['total_price'])
    }

    _getCartItemBySku(sku, cartInfo) {
        for (let item of cartInfo['cart_items']) {
            if (item['product']['sku'] === sku) {
                return item
            }
        }
    }

    _request (method, url='', body='') {
        const params = {
            method:method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            }};
        if (body) {
            params['body'] = JSON.stringify(body);
        }

        return  fetch(this.baseUrl +url+'/', params)
    }

}

new Cart(document.body)