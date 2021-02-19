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
