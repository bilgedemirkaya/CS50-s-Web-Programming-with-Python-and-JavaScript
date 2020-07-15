           // you can design this code better
           document.addEventListener("DOMContentLoaded",function(){
            document.querySelector('#red').onclick = function(){
                document.querySelector('#hello').style.color = 'red';
            }
            document.querySelector('#green').onclick = function(){
                document.querySelector('#hello').style.color = 'green';
            }
            document.querySelector('#blue').onclick = function(){
                document.querySelector('#hello').style.color = 'blue';
            }
            
        });
        /* alternate way to do this: 
         document.addEventListener("DOMContentLoaded",function(){
             document.querySelectorAll('button').ForEach(function(button)) {
                 button.onclick = function(){
                     document.QuerySelector('#hello').style.color = button.dataset.color;
                    }
                 }
             }
        
        */
       //dataset.color takes the button access its data set
       // instead of calling function you can also do:
       // ForEach(button => { 
           // () =>    