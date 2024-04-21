const cep = document.querySelector('#id_zip_code');
const cidade = document.querySelector('#id_city');
const uf = document.querySelector('#id_state');
const bairro = document.querySelector('#id_neighborhood');
const rua = document.querySelector('#id_street');

function limparCampos() {
    cidade.value = '';
    uf.value = '';
    bairro.value = '';
    rua.value = '';
}

cep.addEventListener('input', async () => {
    if (cep.value.length == 9) {
        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep.value}/json/`);
    
            if (!response.ok) {
                throw await response.json();
            }
    
            const responseCep = await response.json();
    
            cidade.value = responseCep.localidade;
            uf.value = responseCep.uf;
            bairro.value = responseCep.bairro;
            rua.value = responseCep.logradouro;
            
        } catch (error) {
           Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Ocorreu um erro ao processar sua solicitação. Por favor, insira um CEP válido.',
        });
        }
    } else {
        limparCampos();
    }
});

cep.addEventListener('keyup', async (event) => {
    if (event.keyCode === 8 || event.keyCode === 46) {
        limparCampos();
    }
});