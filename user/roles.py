from rolepermissions.roles import AbstractUserRole

class clinica(AbstractUserRole):
    available_permissions = {
        'can_view_pacientes': True,
        'can_view_odontogramas': True,
        'can_view_agendas': True,
    }
    
    
    
    