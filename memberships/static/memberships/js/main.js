const hello = () => console.log("hello"); // for debugging

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

// check user's light/dark mode preference
function checkDarkMode() {
  switch (localStorage.getItem("theme")) {
    case "light":
      document.body.classList.remove("dark-mode");
      break;
    case "dark":
      document.body.classList.add("dark-mode");
      break;
    default:
      if (prefersDarkScheme.matches)
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
