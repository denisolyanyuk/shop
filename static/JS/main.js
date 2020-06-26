
document.querySelector("#truck-nearby-tab-bar-tabpane-OWN .tn__multiply-filter_form").addEventListener('submit', function () {
    setTimeout(function () {
        console.log("working")
        console.log("working")
        console.log("working")
        console.log("working")
        let rows = document.querySelectorAll("tbody>tr")
        rows.forEach(row => {
            switch(row.querySelector("td:nth-child(2) i").classList.value) {
            case 'fa fa-road icon-yellow':  // if (x === 'value1')
                row.style.setProperty("background-color","#fffcc9")
                break;
            case 'fa fa-check icon-green':  // if (x === 'value2')
                row.style.setProperty("background-color","#cdffc9")
                break;
            case "fa fa-clock-o icon-blue":  // if (x === 'value2')
                row.style.setProperty("background-color","#c9fffc")
                break;

            }

        })
    },0)
})