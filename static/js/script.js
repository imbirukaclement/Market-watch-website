let items = document.getElementById('navbarSupportedContent').querySelectorAll('ul li a')
function myFunc(m3) {
    if (m3.matches) { // if media query matches
      for (var item = 0; item < items.length; item++){
        items[item].classList.remove('nav-link');
        items[item].classList.add('bt');
        items[item].style.display = "block";
        items[item].style.width = "100px";
      }
    }
}
var m3 = window.matchMedia("(min-width: 992px)"); // media query
myFunc(m3);
