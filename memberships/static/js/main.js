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
      else
        document.documentElement.classList.remove("dark");
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

// toggle visibility of header menu on smaller screens
function toggleHeaderMenu() {
  document.getElementById("header-nav").classList.toggle("hidden");
}

// show popover help text
function showHelpText(popover) {
  let classList = popover.classList;
  
  classList.remove("hidden");

  correctOffscreenRight(popover.firstElementChild);

  classList.remove("opacity-0", "animate-fade-out");
  classList.add("animate-fade-in");
}

// hide popover help text
function hideHelpText(popover) {
  let classList = popover.classList;

  classList.remove("animate-fade-in");
  classList.add("opacity-0", "animate-fade-out");
}

// stop displaying popover if opacity is 0
function hideIfTransparent(popover) {
  let classList = popover.classList;

  if (classList.contains('opacity-0'))
    classList.add('hidden');
}

// check if an element is offscreen to the right and translate if necessary
function correctOffscreenRight(element) {
  let rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
  let classList = element.classList;

  // remove any existing translation
  classList.remove(element.className.split(" ").find((a) => a.startsWith("-translate-x-")));

  // get offscreen distance of element in rem units
  let paddingRight = parseInt(window.getComputedStyle(element, null).getPropertyValue('padding-right'));
  let offscreenRight = (element.getBoundingClientRect().right + paddingRight - window.screen.width) / rootFontSize + 0.5;
  
  // translate element if offscreen
  if (offscreenRight > 0)
    classList.add("-translate-x-" + (Math.floor(offscreenRight) * 4));
}
