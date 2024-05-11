$(document).ready(function() {
    // Ao clicar em uma face do dente ou no quadrado
    $('.face-dente-cima, .face-dente-direita, .face-dente-baixo, .face-dente-esquerda, .quadrado').click(function() {
        // Obtém os dados do dente e da face clicados
        var dente = $(this).data('dente');
        var face = $(this).hasClass('quadrado') ? 'quadrado' : $(this).data('face');
        
        // Preenche o formulário do modal com os dados do dente e da face
        $('#id_number_tooth').val(dente);
        $('#id_tooth_face').val(face);
        
        // Abre o modal
        $('#FormProcedure').modal('show');
    });
    
    // Ao submeter o formulário do modal
    $('#modal-form').submit(function(event) {
        event.preventDefault(); // Impede o envio do formulário padrão
        
        // Obtém os dados do formulário
        var procedure = $('#id_procedure').val();
        var description = $('#id_description').val();
        var color = $('#id_color').val();
        var number_tooth = $('#id_number_tooth').val();
        var tooth_face = $('#id_tooth_face').val();
        var quadrado_dente = $('.quadrado[data-dente="' + dente + '"]');
        
        // Envia os dados via AJAX para o servidor
        $.ajax({
            type: "POST",
            url: "/url/para/o/seu/view/",
            data: {
                procedure: procedure,
                description: description,
                color: color,
                number_tooth: number_tooth,
                tooth_face: tooth_face
            },
            success: function(data) {
                // Fecha o modal
                $('#FormProcedure').modal('hide');
                
                // Define a cor da face do dente clicado
                $('.face-dente-' + tooth_face).css('background-color', color);
                
                // Define a cor do quadrado correspondente à coroa do dente
                quadrado_dente.css('background-color', color);
            }
        });
    });
});
