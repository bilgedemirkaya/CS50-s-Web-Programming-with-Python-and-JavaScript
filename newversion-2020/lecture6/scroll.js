// Add an event listener 

window.onscroll = () => {                              // Listens when user scrolling
    if(window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        // I reached the end of the page
        document.querySelector("body").style.backgroundColor = "green";
    }
    else{
        // Not reached the end yet
        document.querySelector("body").style.backgroundColor = "white";

    }
}
 