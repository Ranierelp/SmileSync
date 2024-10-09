from django import template

register = template.Library()

@register.simple_tag
def procedimento_cor(procedures, dente, face):
    """
    Recebe uma lista de procedimentos já carregados e retorna a cor do procedimento
    para um dente e face específicos.
    """
    for procedure in procedures:
        if procedure.number_tooth == dente and procedure.tooth_face == face:
            return procedure.color
    return ''


