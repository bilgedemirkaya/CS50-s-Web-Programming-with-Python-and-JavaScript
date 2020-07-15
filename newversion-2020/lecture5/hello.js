function hello() {
    const heading = document.querySelector('h1')
    // If we are going to assign a variable that never changes we can call it const intead of let
    if (heading.innerHTML === 'Hello!'){
    heading.innerHTML = 'Goodbye!'; 
     } else {
        heading.innerHTML = 'Hello!'; 
    }
}