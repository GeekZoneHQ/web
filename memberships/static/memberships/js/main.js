let hello = () => console.log("hello");

let header = document.getElementsByClassName("header-container");
let sticky = header[0].offsetTop;

window.onscroll = function() {toggleSticky()};
toggleSticky();

/*** Functions ***/

function toggleSticky() {
  if (window.pageYOffset > sticky) {
    header[0].classList.add("sticky");
  } else {
    header[0].classList.remove("sticky");
  }
}
