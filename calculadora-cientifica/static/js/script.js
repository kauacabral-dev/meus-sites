 
  document.addEventListener('DOMContentLoaded', () => {
        const select = document.getElementById("escolha");
        const campos = document.querySelectorAll(".campo");
        const form = document.getElementById('calcForm');

        function mostrarCampo() {
          const valor = select.value;
          campos.forEach(c => {
            if (c.id === valor) {
              c.style.display = 'block';
              c.querySelectorAll('input, select, textarea').forEach(el => el.disabled = false);
              window.scrollTo({ top: c.offsetTop - 20, behavior: 'smooth' });
            } else {
              c.style.display = 'none';
              c.querySelectorAll('input, select, textarea').forEach(el => el.disabled = true);
            }
          });
        }

       
        form.addEventListener('submit', (ev) => {
          mostrarCampo();
        });

        select.addEventListener('change', mostrarCampo);
        mostrarCampo();
      });

document.getElementById('escolha').addEventListener('change', function() {
    var resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = '';
    resultadoDiv.style.display = 'none'; 
});
