const hello = () => console.log("hello");
var header;

// if scrolled down, make header sticky
function checkSticky() {
  if (!header)
    header = document.getElementsByClassName("header-container")[0];
  
  if (window.pageYOffset > header.offsetTop) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}

// check user's light/dark mode preference
function checkDarkMode() {
  if (localStorage.getItem("theme") == "dark") {
    document.body.classList.add("dark-mode");
  }
}

// change between light and dark modes
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  
  let theme = "light";
  
  if (document.body.classList.contains("dark-mode"))
    theme = "dark";
  
  localStorage.setItem("theme", theme);
}
