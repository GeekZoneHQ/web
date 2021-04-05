const hello = () => console.log("hello"); // for debugging

// check user's light/dark mode preference
function checkDarkMode() {
  switch (localStorage.theme) {
    case "light":
      document.documentElement.classList.remove("dark");
      break;
    case "dark":
      document.documentElement.classList.add("dark");
      break;
    default:
      if (window.matchMedia("(prefers-color-scheme: dark)").matches)
        document.documentElement.classList.add("dark");
  }
}

// change between light and dark modes
function toggleDarkMode() {
  document.documentElement.classList.toggle("dark");
  
  if (document.documentElement.classList.contains("dark"))
    localStorage.theme = "dark";
  else
    localStorage.theme = "light";
}

// toggle visibility of help-text
function toggleHelpText(fieldName) {
  let classes = document.getElementsByClassName(fieldName + "-help-text")[0].classList;
  
  // accounting for first iteration
  if (classes.contains("opacity-0"))
    classes.remove("animate-fade-out");
  else
    classes.add("animate-fade-out");

  classes.toggle("animate-fade-in");
  classes.toggle("opacity-0");
}

// toggle visibility of header menu on smaller screens
function toggleHeaderMenu() {
  document.getElementById("header-nav").classList.toggle("hidden");
}
