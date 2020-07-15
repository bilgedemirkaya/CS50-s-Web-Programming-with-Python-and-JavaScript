           // you can design this code better
           document.addEventListener("DOMContentLoaded",function(){
            document.querySelector("select").onchange = function(){
                document.querySelector("#hello").style.color = this.value;
            }
        });
        /* Events:
        onclick
        onmouseover
        onkeydown -- keyboard event
        onkeyup -- keyboard event
        onload
        onblur
         */