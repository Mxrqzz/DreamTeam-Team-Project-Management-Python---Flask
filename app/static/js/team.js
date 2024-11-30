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

//Mostra o formulario
function show_form() {
  document.getElementById("form-box").classList.remove("hidden");  
  document.getElementById("members_team").classList.add("hidden");  
  document.getElementById("button-form").classList.add("hidden");
}

//Fecha o formulario
function close_form() {
  document.getElementById("form-box").classList.add("hidden");  
  document.getElementById("members_team").classList.remove("hidden");  
  document.getElementById("button-form").classList.remove("hidden");
}

