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
    #rfc = fields.Char()
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
    
    zoho_files = fields.One2many('crm.zoho','crm_id',string="Archivos")

   
    estado = fields.Many2one('direcciones.estados',string="Estado")
    municipio = fields.Many2one('direcciones.municipios', string="Municipio")
    archivo_base64 = fields.Char()
    @api.onchange('estado')
    def filter_munic(self):
        return {'domain': {'municipio': [('id_estado','=', self.estado.id)]}}

    """Campos para insertar o actualizar una oficina"""
    check_zoho_id = fields.Boolean(string="¿Cuentas con Zoho ID?")
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
    #importe_zoho = fields.Char('Importe')
    respuesta_err = fields.Char()
    """Funciones para las distintas operaciones permitidas en zoho"""

    # def inserta_oficina(self):
    #     url = "https://sandbox.zohoapis.com/crm/v2/functions/masterbroker_inserta_oficina_v1/actions/execute?auth_type=apikey&master_broker_token=chlestiustiayiecrlucroewiaphlar2&zapikey=1003.0493b2f5bf95786ae1461418498f0f32.42839246fcebd5e3f45ccd7b1cdebad7"
    #     if not self.nombre_oficina :
    #         raise UserError("Nombre de la oficina no definido")
    #     if not self.telefono_oficina :
    #         raise UserError("Telefono de la oficina no definida")
    #     if not self.calle_num_oficina :
    #         raise UserError("Calle y número de la oficina no definido")
    #     if not self.colonia_oficina :
    #         raise UserError("Colonia de la oficina no definido")
    #     if not self.delegacion_oficina:
    #         raise UserError("Delegación de la no definido")
    #     if not self.estado_oficina :
    #         raise UserError("Estado Oficina no definido")
    #     if not self.cp_oficina :
    #         raise UserError("Codigo Postal Oficina definido")
    #     if not self.correo_oficina:
    #         raise UserError("Correo de la oficina no definido")
    #     if not self.sitio_web_oficina:
    #         raise UserError("Sitio Web de la oficina no definida")

    #     payload = json.dumps({
    #     {
    #         "zoho_id": self.zoho_id if self.zoho_id else "",
    #         "oficina_nombre": self.nombre_oficina,
    #         "oficina_telefono":self.telefono_oficina,
    #         "oficina_calle_y_no": self.calle_num_oficina,
    #         "oficina_colonia": self.colonia_oficina,
    #         "oficina_delegacion_municipio": self.delegacion_oficina,
    #         "oficina_estado": self.estado_oficina,
    #         "oficina_codigo_postal": self.cp_oficina,
    #         "oficina_correo_electronico": self.correo_oficina,
    #         "oficina_sitio_web": self.sitio_web_oficina,
    #     }
    #     })
    #     headers = {
    #     'zapikey': '1003.cc7584ca319e65e957f32ce61e2f1502.fbabf6196572fa59f4c3fc203c967318',
    #     'Content-Type': 'application/json'
    #     }

    #     response = requests.request("POST", url, headers=headers, data=payload)

    #     logger.info(response.text) 

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
            # respuesta = (response.content)
            # respuesta= json.load(respuesta)
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
    archivo = fields.Binary('Archivo')
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
