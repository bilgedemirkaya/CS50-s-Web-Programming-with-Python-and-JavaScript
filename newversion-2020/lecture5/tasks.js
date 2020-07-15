document.addEventListener("DOMContentLoaded",function(){

    //if user press submit button with empty string it will create a empty li, to prevent this, enable the submit button:
    document.querySelector("#submit").disabled = true;


    // If user type smth and delete it, it will still disable the submit button when the length is 0
    document.querySelector("#task").onkeyup = () => {  
        if (document.querySelector('#task').value.length > 0 ){
            document.querySelector("#submit").disabled = false;
        }
        else {
            document.querySelector("#submit").disabled = true;
        } 
    }

    document.querySelector('form').onsubmit = () => {
       const task = document.querySelector('#task').value;
       
       // If I am curious what the user typed in I can print it out in the console like: 
       console.log(task);

        // we created a new element called li and filled it with const task
       const li = document.createElement('li');
       li.innerHTML = task;

       //append the li element into the task
       document.querySelector('#tasks').append(li);
        
       // this will clear the input field
       document.querySelector('#task').value = ' ';
       // After submittin one task disable the submit button again till user type smth
       document.querySelector("#submit").disabled = true;
    

       // To stop form submitting:
       return false; // that means dont submit form anywhere we will do everything in the browser

    }

})