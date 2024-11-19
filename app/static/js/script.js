// Seleciona o botão e o corpo do documento
const toggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Função para aplicar o tema
function applyTheme(theme) {
  body.className = theme; // Define a classe no body
}

// Verifica se há uma preferência de tema salva no localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
  applyTheme(savedTheme);
} else {
  // Define o modo claro como padrão, se nenhum tema estiver salvo
  applyTheme('light-mode');
}

// Adiciona o evento de clique para alternar o tema
toggleButton.addEventListener('click', () => {
  const newTheme = body.classList.contains('light-mode') ? 'dark-mode' : 'light-mode';
  applyTheme(newTheme);
  localStorage.setItem('theme', newTheme); // Salva a preferência no localStorage
});
