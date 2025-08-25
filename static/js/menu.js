const toggle = document.getElementById("menu-toggle");
const menu = document.getElementById("side-menu");

  toggle.addEventListener("click", () => {
    if (menu.style.display === "block") {
      menu.style.display = "none";
    } else {
      menu.style.display = "block";
    }
  });

  document.addEventListener("click", function (event) {
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      menu.style.display = "none";
    }
  });