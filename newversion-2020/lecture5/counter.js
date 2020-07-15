
if (!localStorage.getItem('counter')){
   localStorage.setItem('counter',0);
}
// now we will use localstorage instead of variable let counter = 0;
function count() {
counter = localStorage.getItem('counter');
counter++;
document.querySelector('h1').innerHTML = counter;
localStorage.setItem('counter',counter);  //save the lst value of counter
//if (counter % 10 === 0)
//{
   // alert ( f{"count is now {counter}" ) this is how we would do this in python
  // alert(`Count is now ${counter}`) //template literal, ${ } means plug in a variable here
//}
}

// document.querySelector('button').onclick = count;
// I am not actually calling the function if i call it i would do count(), but I am setting litterally equal to the function itself

// It is not going to work bcs js code looking for button but body of the page hasnt finished loading yet.
//I can add an event listener to the document itself

document.addEventListener('DOMContentLoaded',function(){
   //so now when refresh the page, it'll go back to value that remembered not 0, bcs h1 was 0 in html code.
document.querySelector('h1').innerHTML =localStorage.getItem('counter');
document.querySelector('button').onclick = count;

// run this function every 1000 miliseconds
//setInterval(count,1000);
});
/* It says, wait until the all the content in the page is loaded, then run this function, so now we will able to find the button
So now I am able to seperate all of my js code from the html, you can move js to seperate file
To do this: in the head <script src='counter.js'></cript> */

/* Now our code doesnt store any information. There is a way to remembering information for later use, Now js allows us to do smth called 
local storage. Its a way for us to store info inside of the users web browser 

Local storage is gonna give access to two key functions that we will use to manipulate this local storage:
1) localstorage.getItem(key)
2) localstorage.setItem(key,value)
*/
