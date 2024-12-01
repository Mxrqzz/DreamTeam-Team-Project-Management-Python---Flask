document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('main section');
  const menuItems = document.querySelectorAll('.sidebar li');

  menuItems.forEach(item => {
    item.addEventListener('click', () => {
      const sectionToShow = item.getAttribute('data-section');

      //Ocultar todas as sessões
      sections.forEach(section => section.classList.add('hidden'));

      //Mostra apenas a sessão selecionada
      document.getElementById(sectionToShow).classList.remove('hidden');
    });
  });
});

function show_cargo() {
  const button_alter = document.getElementById("button-alter");
  const button_edit = document.getElementById("button-editar");
  const radio = document.getElementById("radio");

  // Exibe os botões de Cancelar e Salvar
  button_alter.classList.remove("hidden");
  radio.classList.remove("hidden");

  // Esconde o botão "Editar" específico
  button_edit.classList.add("hidden");
}

function close_cargo() {
  const button_alter = document.getElementById("button-alter");
  const button_edit = document.getElementById("button-editar");
  const radio = document.getElementById("radio");

  // Esconde os botões de Cancelar e Salvar
  button_alter.classList.add("hidden");
  radio.classList.add("hidden");

  // Exibe o botão "Editar" específico
  button_edit.classList.remove("hidden");
}


function show_form() {
  const formBox = document.getElementById("form-box");
  const addUserImage = document.getElementById("add-user-image");

  formBox.classList.remove("hidden");
  addUserImage.classList.remove("hidden"); // Mostra a imagem

  // Esconde os membros e o botão "Convidar Membros"
  document.querySelectorAll(".members-team").forEach(member => {
    member.classList.add("hidden");
  });
  document.getElementById("button-form").classList.add("hidden");
}

// Fecha o formulário e esconde a imagem
function close_form() {
  const formBox = document.getElementById("form-box");
  const addUserImage = document.getElementById("add-user-image");

  formBox.classList.add("hidden");
  addUserImage.classList.add("hidden"); // Esconde a imagem

  // Mostra os membros e o botão "Convidar Membros"
  document.querySelectorAll(".members-team").forEach(member => {
    member.classList.remove("hidden");
  });
  document.getElementById("button-form").classList.remove("hidden");
}

function show_form_project() {
  const formBox = document.getElementById("project-form");
  const addUserImage = document.getElementById("add-user-image");

  formBox.classList.remove("hidden");
  addUserImage.classList.remove("hidden"); // Mostra a imagem

  // Esconde os membros e o botão "Convidar Membros"
  document.querySelectorAll(".projetos").forEach(member => {
    member.classList.add("hidden");
  });
  document.getElementById("button-form").classList.add("hidden");
}

// Fecha o formulário e esconde a imagem
function close_form_project(){
  const formBox = document.getElementById("project-form");
  const button_create = document.getElementById("create_project");

  formBox.classList.add("hidden");
  button_create.classList.remove("hidden");

  // Mostra os membros e o botão "Convidar Membros"
  document.querySelectorAll(".projetos").forEach(member => {
    member.classList.remove("hidden");
  });
  document.getElementById("button-form").classList.remove("hidden");
}

