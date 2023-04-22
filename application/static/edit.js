const toggleEditForm = () => {
    const nameDiv = document.querySelector("#name-div");
    const nameForm = document.querySelector("#edit-name-div");
    nameDiv.classList.toggle("d-none");
    nameForm.classList.toggle("d-none");
}

const editButton = document.querySelector("#edit-name");
editButton.addEventListener("click", toggleEditForm);
const cancelEditButton = document.querySelector("#cancel-edit-name");
cancelEditButton.addEventListener("click", toggleEditForm);
