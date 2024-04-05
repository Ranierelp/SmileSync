from rolepermissions.roles import AbstractUserRole

class Clinica(AbstractUserRole):
    available_permissions = {
        'can_view_pacientes': True,
        'can_view_odontogramas': True,
        'can_view_relatorios': True,
        'can_view_dentistas': True,
        'can_view_empresas': True,
    }
    
    
    