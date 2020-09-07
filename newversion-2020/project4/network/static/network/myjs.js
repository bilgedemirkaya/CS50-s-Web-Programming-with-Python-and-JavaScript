function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.profilebutton')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
      // Use buttons to toggle between views
      document.querySelector('#posts').addEventListener('click', () => show_page('posts'));
      document.querySelector('#likes').addEventListener('click', () => show_page('likes'));
  });