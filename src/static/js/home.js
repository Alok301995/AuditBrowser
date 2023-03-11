// ************************************************************************************************

ham_icon = document.getElementById("ham-icon");
close_icon = document.getElementById("close-icon");
side_menu = document.getElementById("side-menu");

ham_icon.addEventListener("click", hamHandler);
close_icon.addEventListener("click", closeHandler);

function hamHandler() {
  ham_icon.classList.toggle("animate-all");
  ham_icon.style.display = "none";
  close_icon.style.display = "block";
  side_menu.style.display = "block";
}
function closeHandler() {
  close_icon.style.display = "none";
  ham_icon.style.display = "block";
  side_menu.style.display = "none";
}


