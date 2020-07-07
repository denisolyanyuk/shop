

let form = document.getElementById('form');
let paymentBtn = document.getElementById('make-payment');
form.addEventListener('submit', submitForm)
paymentBtn.addEventListener('click', makePayment)

function submitForm(event){
    event.preventDefault();
    document.getElementById('form-button').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
}

function makePayment() {

}



