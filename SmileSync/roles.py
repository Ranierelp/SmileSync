from rolepermissions.roles import AbstractUserRole

class Clinica(AbstractUserRole):
    available_permissions = {
        'can_view_pacientes': True,
        'can_edit_pacientes': True,
        'can_create_pacientes': True,
        'can_delete_pacientes': True,
        'can_view_medical_record': True,
        
        'can_view_empresa': True,
        'can_edit_empresa': True,
        'can_create_empresa': True,
        'can_delete_empresa': True,
        
        'can_view_denstista': True,
        'can_edit_denstista': True,
        'can_create_denstista': True,
        'can_delete_denstista': True,
        
    }
    
class Dentista(AbstractUserRole):
    available_permissions = {
        'can_view_pacientes': True,
        'can_edit_pacientes': True,
        'can_delete_pacientes': True,
        'can_view_medical_record': True,
        'can_create_medical_record': True,
        
        'can_view_empresa': True,
        'can_edit_empresa': True,
        'can_create_empresa': True,
        'can_delete_empresa': True,
        
        'can_view_denstista': True,
        'can_edit_denstista': True,
        'can_create_denstista': True,
        'can_delete_denstista': True,
    }
    
class Empresa(AbstractUserRole):
    available_permissions = {
        'can_view_pacientes': True,
        'can_edit_pacientes': True,
        'can_create_pacientes': True,
        'can_delete_pacientes': True,
        
        'can_edit_empresa': True,
    }
    