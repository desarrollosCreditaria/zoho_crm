# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api
import requests
import json
from odoo.exceptions import UserError
import logging
from base64 import b64decode
from datetime import datetime
from pytz import timezone
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)
class CrmLead(models.Model):
    _inherit = "crm.lead"
  
    """Campos para insertar una operación"""
    nombre = fields.Char()
    ap_paterno = fields.Char()
    ap_materno = fields.Char()
    banco = fields.Selection([
        ('Afirme', 'Afirme'),
        ('Autofin', 'Autofin'),
        ('Banamex', 'Banamex'),
        ('Banca MIFEL', 'Banca MIFEL'),
        ('Banco Inmobiliario Mexicano', 'Banco Inmobiliario Mexicano'),
        ('Banco Ve por Mas', 'Banco Ve por Mas'),
        ('Banorte', 'Banorte'),
        ('BBVA Bancomer', 'BBVA Bancomer'),
        ('Hey Banco', 'Hey Banco'),
        ('HSBC', 'HSBC'),
        ('Inbursa', 'Inbursa'),
        ('Infonavit', 'Infonavit'),
        ('ION', 'ION'),
        ('Santander', 'Santander'),
        ('Scotiabank', 'Scotiabank'),
        ('TU CASA EXPRESS', 'TU CASA EXPRESS'),


    ], string='banco')
    
    zoho_files = fields.One2many('crm.zoho','crm_id',string="Caratula Zoho")

   
    estado = fields.Many2one('direcciones.estados',string="Estado")
    municipio = fields.Many2one('direcciones.municipios', string="Municipio")
    @api.onchange('estado')
    def filter_munic(self):
        return {'domain': {'municipio': [('id_estado','=', self.estado.id)]}}

    """Campos para insertar o actualizar una oficina"""
    zoho_id = fields.Char()
    nombre_oficina = fields.Char('Nombre de la oficina')
    telefono_oficina = fields.Char('Télefono de la oficina')
    calle_num_oficina = fields.Char('Calle y Número')
    colonia_oficina = fields.Char('Colonia')
    delegacion_oficina = fields.Char('Delagación')
    estado_oficina = fields.Char('Estado')
    cp_oficina = fields.Char('Código Postal')
    correo_oficina = fields.Char('Correo electrónico')
    sitio_web_oficina = fields.Char('Sitio web')
    respuesta_err = fields.Char()
    caratula_zoho = fields.Binary('Caratula Zoho')

    """Funciones para las distintas operaciones permitidas en zoho"""

    def inserta_operacion(self):
        try :
            zapikey ="1003.bc36ba6d6dc90970df9a80a939394c75.349e99da76368fc4e08ea9b37947335b"
            master_broker_token ="chlestiustiayiecrlucroewiaphlar2"
          
            url = " https://www.zohoapis.com/crm/v2/functions/masterbroker_inserta_operacion_v1/actions/execute?auth_type=apikey&master_broker_token="+master_broker_token+"&zapikey="+zapikey
            crm = self.env['crm.lead'].search([('id','=',self.id)],limit=1)
            user= self.env['res.users'].search([('id','=',self.env.uid)])
            if not user.zoho_id:
                raise UserError("Zoho ID  no definido, contacta al administrador")
            if not self.nombre :
                raise UserError("Nombre no definido")
            if not self.ap_paterno :
                raise UserError("Apellido Paterno no definido")
            if not self.ap_materno :
                raise UserError("Apellido Materno no definido")    
            if not self.x_rfc :
                raise UserError("RFC no definido")          
            if not self.banco :
                raise UserError("Banco no definido")
            if not self.estado:
                raise UserError("Estado no definido")
            if not self.municipio :
                raise UserError("Municipio no definido")
            if not self.expected_revenue :
                raise UserError("Importe no definido")
            data = {"nombre": self.nombre,
                    "apellido_paterno":self.ap_paterno,          
                    "apellido_materno":self.ap_materno,
                    "rfc" : self.x_rfc,
                    "importe":self.expected_revenue,
                    "banco":self.banco,
                    "entidad_federativa":self.estado.d_estado,
                    "municipio":self.municipio.d_municipio,
                     "asesor_id":user.zoho_id}
            payload = json.dumps(data)
            logger.info(payload)
            headers = {
            'zapikey': zapikey,
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            response = json.loads(response.content,strict=False)
            if 'error' in response: 
                raise UserError(response)
            if 'pdf' in response:
                archivo=response['pdf']
                self.env['crm.zoho'].sudo().create({'crm_id': crm.id, 'archivo' :archivo, 'fecha_creacion': datetime.now().astimezone(timezone('America/Mexico_City'))})
            else:
                raise UserError(response)
        except Exception as err:
            raise UserError(err)
    
class archivosZoho(models.Model):

    _name="crm.zoho"
    _description="Files Zoho"
    _order='create_date desc'

    crm_id = fields.Many2one('crm.lead',string='Oportunidad')
    archivo = fields.Binary('Zoho Caratula')
    filename_archivo = fields.Char()
    fecha_creacion = fields.Date('Fecha de creación')
    
    @api.model
    def create(self,values):
        return super(archivosZoho,self).create(values)
    @api.model
    def write(self,values):
        return super(archivosZoho,self).write(values)

class ResUsers(models.Model):
    _inherit='res.users'
    
    zoho_id = fields.Char("Zoho ID")

    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'zoho_id' in vals:
            
            return super(ResUsers, self).write(vals)
