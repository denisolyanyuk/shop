class Cart {
    baseUrl = `${location.protocol}//${location.host}/api/cart/`
    csrfToken = (window.user === "AnonymousUser") ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value :
        getCookie('csrftoken');

    async updateCartInNavBar() {
        let cartTotalElem = document.getElementById('cart-total-items');
        const response = this.#request('GET', 'quantity_of_items/')
        let data = await response.json()
        cartTotalElem.innerHTML = data['total_quantity']
    }

    async updateItem(sku, action) {
        await this.#request('PATCH', action+'/', {'sku':sku})
    }

    async getItems(){
        await this.#request('GET')
    }

    async #request(method, url='', body='') {
        const response = await fetch(this.baseUrl + url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
            body: JSON.stringify(body)

        })
        await response
    }

}

