document.addEventListener("DOMContentLoaded",function(){
    const h1 = document.querySelector('h1');
    h1.style.animationPlayState = 'paused';

    document.querySelector('button').onclick = () => {
        if(h1.style.animationPlayState === "paused"){
            h1.style.animationPlayState = 'running';
        }
        else{
            h1.style.animationPlayState = 'paused';
        }
    }

})