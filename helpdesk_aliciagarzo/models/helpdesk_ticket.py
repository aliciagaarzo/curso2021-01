from odoo import models, fields
class HelpdeskTicket(models.Model):
    _name= 'helpdesk.ticket'

    name= fields.Char(string='Name', requiered = True)
    description=fields.Text(string='Description')
    date=fields.Date(string='Date')

    state= fields.Selection( 
        [('nuevo', 'Nuevo'), 
        ('asignado', 'Asignado'),
        ('proceso', 'Proceso'),
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
        ('cancelado', 'Cancelado')],
        string = 'State', default='nuevo') 

#Tiempo dedicado (en horas)
    time = fields.Float(string='Time')


    date_limit = fields.Date(string='Date Limit')

    assigned = fields.Boolean(string='Assigned', readonly=True)

    action_corrective = fields.Html(string='Corrective Action', help='Descrive corrective actions to do')

    action_preventive = fields.Html(string='Preventive Action', help='Descrive corrective actions to do')