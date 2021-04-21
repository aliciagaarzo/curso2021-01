from odoo import models, fields, api

class HelpdeskTicketAction(models.Model):
    _name= 'helpdesk.ticket.action'
    _description= 'Action'
    
    name= fields.Char()
    date=fields.Date()
    ticket_id=fields.Many2one(
        comodel_name = 'helpdesk.ticket',
        string = 'Ticket'
    )

class HelpdeskTicketTag(models.Model):
    _name= 'helpdesk.ticket.tag'
    _description= 'Tag'
    
    name= fields.Char(string='Name', required = True)
    ticket_id = fields.Many2many(
        comodel_name = 'helpdesk.ticket',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'tag_id',
        column2 = 'ticket_id',
        string = 'Tags'
    )
    
class HelpdeskTicket(models.Model):
    _name= 'helpdesk.ticket'
    _description= 'Ticket'
    
    name= fields.Char(string='Name', requiered = True)
    description=fields.Text(string='Description', translate=True)
    date=fields.Date(string='Date')

    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket.tag',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'ticket_id',
        column2 = 'tag_id',
        string = 'Tags' 
    )

    actions_ids = fields.One2many(
        comodel_name = 'helpdesk.ticket.action',
        inverse_name = 'ticket_id',
        string = 'Actions' 
    )

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

    # Asignado (tipo check)
    # pasamos el campo assigned a ser un campo calculado
    assigned = fields.Boolean(
        string='Assigned', 
        compute='_compute_assigned')

    # Fecha limite
    date_limit = fields.Date(string='Date Limit')

    # Acción correctiva (html)
    action_corrective = fields.Html(string='Corrective Action', help='Descrive corrective actions to do')

    # Acción preventiva (html)
    action_preventive = fields.Html(string='Preventive Action', help='Descrive corrective actions to do')

    # Si no se indica un nombre de tabla se crea automaticamente, por si quieres tener varios campos
    # Many2many en un mismo modelo obliga a indicar un nombre de tabka especifica
    user_id = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Assigned to'
    )

    tag_ids = fields.Many2many(
        comodel_name = 'helodesk.ticket.tag',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'ticket_id',
        column2 = 'tag_id',
        string = 'Tags'
    )

    action_ids = fields.One2many(
        comodel_name = 'helpdesk.ticket.action',
        inverse_name = 'ticket_id',
        string = 'Actions'
    )



    # Metodos// Añadir en el header los siguiente botones:

    #Crear una funcion/ Asignar, cambia estado a asignado y pone a true el campo asignado, visible sólo con estado = nuevo
    
    def asignar(self):
        self.ensure_one()
        self-write({
            'state':'asignado', 'assigned': True})

    # En proceso, visible sólo con estado = asignado

    def proceso(self):
        self.ensure_one()
        self.state = 'proceso'


    #Pendiente, visible sólo con estado = en proceso o asignado

    def pendiente(self):
        self.ensure_one()
        self.state = 'pendiente'


    #Finalizar, visible en cualquier estado, menos cancelado y finalizado

    def finalizar(self):
        self.ensure_one()
        self.state = 'resuelto'

    #Cancelar, visible si no está cancelado

    def cancelar(self):
        self.ensure_one()
        self.state = 'cancelado'

    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False     
    
    #Cada botón pondrá el objeto en el estado correspondiente.



    #Hacer un campo calculado que indique la cantidad de tickets asociados al mismo usuario
    ticket_qty = fields.Integer(
        string = 'Ticket Qty',
        compute = '_compute_ticket_qty'
        )


    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)


    # Crear un campo de etiqueta y hacer un boton que cree la nueva etiqueta con ese nombre y lo asocie al ticket

    tag_name = fields.Char(
        strings='Tag name')

    def create_tag(self):
        self.ensure_one()
        # opcion 1
        self.write({
            'tag_ids': [(0,0, {'name':self.tag_name})]
            })

        self.tag_name = False