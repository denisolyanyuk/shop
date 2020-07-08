

let form = document.getElementById('form');
let paymentBtn = document.getElementById('make-payment');
form.addEventListener('submit', submitForm)
paymentBtn.addEventListener('click', processOrder)

function submitForm(event){
    event.preventDefault();
    document.getElementById('form-button').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
}

async function processOrder() {
    const url = `${location.protocol}//${location.host}/process_order/`;
    const csrftoken = getCookie('csrftoken');
    const form = document.getElementById('form');

    const response = await fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({
            'form': Object.fromEntries(new FormData(form).entries()),
        }),
    })
    data = await response.json()
    if (!response.ok) {
        alert(data['message'])
    }



}



