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

function showHelpText(helpTextClassList) {
  helpTextClassList.remove("opacity-0");
  helpTextClassList.remove("animate-fade-out");
  helpTextClassList.add("animate-fade-in");
}

function hideHelpText(helpTextClassList) {
  helpTextClassList.add("opacity-0");
  helpTextClassList.add("animate-fade-out");
  helpTextClassList.remove("animate-fade-in");
}

// toggle visibility of header menu on smaller screens
function toggleHeaderMenu() {
  document.getElementById("header-nav").classList.toggle("hidden");
}
