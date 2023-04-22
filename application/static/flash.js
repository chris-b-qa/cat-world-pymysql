const hideFlashes = (event) => {
  const flashes = document.querySelector('.flashes');
  flashes.classList.add('d-none');
};

const closeFlashesButton = document.querySelector("#close-flashes");
if (closeFlashesButton !== null) {
  closeFlashesButton.addEventListener("click", hideFlashes);
}