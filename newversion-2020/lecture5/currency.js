document.addEventListener("DOMContentLoaded",() => {

    document.querySelector("form").onsubmit = () => {

    // fetch is going to do web request,ang get back Http response from that page
    fetch('https://api.exchangeratesapi.io/latest?base=USD')

    // what fetch is going to give us is a promise.It means that smth is going to back but it may not come back immediately
    //.then means what should i do when the promises is come back
    .then(response => {
        return response.json(); // convert response to json format
    } )

    // if you have a function that takes smth and returning smth else, you can simplify the coding :
    // .then(response => response.json())

    .then(data => {
       // console.log(data) -- print it out to terminal

       // what user typed in the form
       const currency = document.querySelector('#currency').value.toUpperCase();
        const rate = data.rates[currency]; // I cant do data.rates.currency bcs currency is a variable
        if (rate !== undefined ) {
            document.querySelector('#result').innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}.`; // round it to 3 decimal point
        }
        else{
            document.querySelector('#result').innerHTML="No such a currency rate";
        }
    })
    //If something goes wrong taking the API data, give a error message
    .catch(error => {
        console.log('Error',error);
    })

        return false; // we dont actually trying to submit the form, we"ll handle it locally.
    }
    })