document.addEventListener('DOMContentLoaded', function() {
    var cnpjtElement = document.getElementById('id_cnpj');

    if (cnpjtElement) {
        cnpjtElement.addEventListener('input', function(event) {
            var cnpj = event.target.value.replace(/\D/g, '');
            
            if (cnpj.length > 14) {
                cnpj = cnpj.slice(0, 14);
            }

            var cnpjFormatado = '';
            
            for (var i = 0; i < cnpj.length; i++) {
                if (i === 2 || i === 5) {
                    cnpjFormatado += '.';
                } else if (i === 8) {
                    cnpjFormatado += '/';
                } else if (i === 12) {
                    cnpjFormatado += '-';
                }
                cnpjFormatado += cnpj.charAt(i);
            }
            
            event.target.value = cnpjFormatado;
        });

    }

});

document.getElementById('id_telefone')?.addEventListener('input', function(event) {
    var telefone = event.target.value.replace(/\D/g, '');
    
    var celular = telefone.length === 11 && telefone.charAt(2) === '9';

    if (celular) {
        if (telefone.length > 11) {
            telefone = telefone.slice(0, 11);
        }
    } else {
        if (telefone.length > 10) {
            telefone = telefone.slice(0, 10);
        }
    }

    var telefoneFormatado = '';
    
    if (celular) {
        telefoneFormatado = '(' + telefone.substring(0, 2) + ') ' + telefone.substring(2, 7) + '-' + telefone.substring(7, 11);
    } else {
        telefoneFormatado = '(' + telefone.substring(0, 2) + ') ' + telefone.substring(2, 6) + '-' + telefone.substring(6, 10);
    }
    
    event.target.value = telefoneFormatado;
});

document.getElementById('id_zip_code')?.addEventListener('input', function(event) {
    var cep = event.target.value.replace(/\D/g, ''); 
    var cepFormatado = '';
    
    for (var i = 0; i < cep.length; i++) {
      if (i === 5) {
        cepFormatado += '-';
      }
      cepFormatado += cep.charAt(i);
    }
    
    event.target.value = cepFormatado;
  });

// Verifica se existe um campo de CPF na página
var campoCpf = document.getElementById('id_cpf');
if (campoCpf) {
    // Se existir, adiciona o ouvinte de evento para formatar o CPF
    campoCpf.addEventListener('input', function(event) {
        var cpf = event.target.value.replace(/\D/g, ''); // Remove todos os não dígitos
        var cpfFormatado = '';
        
        for (var i = 0; i < cpf.length; i++) {
            if (i === 3 || i === 6) {
                cpfFormatado += '.';
            } else if (i === 9) {
                cpfFormatado += '-';
            }
            cpfFormatado += cpf.charAt(i);
        }
        
        event.target.value = cpfFormatado;
    });

    // Limita o tamanho máximo do campo para 14 caracteres
    campoCpf.maxLength = 14;
}
