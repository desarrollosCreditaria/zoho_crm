# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api
import requests
import json
from odoo.exceptions import UserError
import logging
import base64


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
    rfc = fields.Char()
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
    
    entidad_federativa = fields.Selection([
        ('Aguascalientes', 'Aguascalientes'),
        ('Baja California', 'Baja California'),
        ('Baja California Sur', 'Baja California Sur'),
        ('Campeche', 'Campeche'),
        ('Chiapas', 'Chiapas'),
        ('Chihuahua', 'Chihuahua'),
        ('Ciudad de México', 'Ciudad de México'),
        ('Coahuila de Zaragoza', 'Coahuila de Zaragoza'),
        ('Colima', 'Colima'),
        ('Durango', 'Durango'),
        ('Estado de México', 'Estado de México'),
        ('Guanajuato', 'Guanajuato'),
        ('Guerrero', 'Guerrero'),
        ('Hidalgo', 'Hidalgo'),
        ('Jalisco', 'Jalisco'),
        ('Michoacán', 'Michoacán'),
        ('Morelos', 'Morelos'),
        ('Nayarit', 'Nayarit'),
        ('Nuevo León', 'Nuevo León'),
        ('Oaxaca', 'Oaxaca'),
        ('Puebla', 'Puebla'),
        ('Querétaro', 'Querétaro'),
        ('Quintana Roo', 'Quintana Roo'),
        ('San Luis Potosí', 'San Luis Potosí'),
        ('Sinaloa', 'Sinaloa'),
        ('Sonora', 'Sonora'),
        ('Tabasco', 'Tabasco'),
        ('Tamaulipas', 'Tamaulipas'),
        ('Tlaxcala', 'Tlaxcala'),
        ('Veracruz de Ignacio de la Llave', 'Veracruz de Ignacio de la Llave'),
        ('Yucatán', 'Yucatán'),
        ('Zacatecas', 'Zacatecas'),
    ], string='Entidad Federativa')
    municipio = fields.Char()
    archivo_base64 = fields.Char()
    archivo = fields.Binary()

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

    """Funciones para las distintas operaciones permitidas en zoho"""

    def inserta_oficina(self):
        url = "https://sandbox.zohoapis.com/crm/v2/functions/masterbroker_inserta_oficina_v1/actions/execute?auth_type=apikey&master_broker_token=chlestiustiayiecrlucroewiaphlar2&zapikey=1003.0493b2f5bf95786ae1461418498f0f32.42839246fcebd5e3f45ccd7b1cdebad7"
        if not self.nombre_oficina :
            raise UserError("Nombre de la oficina no definido")
        if not self.telefono_oficina :
            raise UserError("Telefono de la oficina no definida")
        if not self.calle_num_oficina :
            raise UserError("Calle y número de la oficina no definido")
        if not self.colonia_oficina :
            raise UserError("Colonia de la oficina no definido")
        if not self.delegacion_oficina:
            raise UserError("Delegación de la no definido")
        if not self.estado_oficina :
            raise UserError("Estado Oficina no definido")
        if not self.cp_oficina :
            raise UserError("Codigo Postal Oficina definido")
        if not self.correo_oficina:
            raise UserError("Correo de la oficina no definido")
        if not self.sitio_web_oficina:
            raise UserError("Sitio Web de la oficina no definida")

        payload = json.dumps({
        {
            "zoho_id": self.zoho_id if self.zoho_id else "",
            "oficina_nombre": self.nombre_oficina,
            "oficina_telefono":self.telefono_oficina,
            "oficina_calle_y_no": self.calle_num_oficina,
            "oficina_colonia": self.colonia_oficina,
            "oficina_delegacion_municipio": self.delegacion_oficina,
            "oficina_estado": self.estado_oficina,
            "oficina_codigo_postal": self.cp_oficina,
            "oficina_correo_electronico": self.correo_oficina,
            "oficina_sitio_web": self.sitio_web_oficina,
        }
        })
        headers = {
        'zapikey': '1003.cc7584ca319e65e957f32ce61e2f1502.fbabf6196572fa59f4c3fc203c967318',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        logger.info(response.text) 

    def inserta_operacion(self):
        url = "https://sandbox.zohoapis.com/crm/v2/functions/masterbroker_inserta_operacion_v1/actions/execute?auth_type=apikey&master_broker_token=chlestiustiayiecrlucroewiaphlar2&zapikey=1003.0493b2f5bf95786ae1461418498f0f32.42839246fcebd5e3f45ccd7b1cdebad7"
        crm = self.env['crm.lead'].search([('id','=',self.id)],limit=1)
        payload = json.dumps( {"nombre": str(self.user_id.partner_id.name),
                "apellido_paterno":str(self.ap_paterno),          
                "apellido_materno":str(self.ap_materno),
                "rfc" : str(self.rfc),
                "importe":"333333",
                "banco": str(self.banco),
                "entidad_federativa":str(self.entidad_federativa),
                "municipio":"Miguel Hidalgo",
                "asesor_id":"4994884000000419919"})
        headers = {
        'zapikey': '1003.cc7584ca319e65e957f32ce61e2f1502.fbabf6196572fa59f4c3fc203c967318',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #logger.info(response.json()['pdf'])
        archivo=response.json()['pdf']
        logger.info(str(archivo))
        #archivo=base64.b64decode(str(archivo))
        #crm.sudo().write({'archivo_base64':archivo})
        
        
        
        
        # url = "https://sandbox.zohoapis.com/crm/v2/functions/masterbroker_inserta_operacion_v1/actions/execute?auth_type=apikey&master_broker_token=chlestiustiayiecrlucroewiaphlar2&zapikey=1003.0493b2f5bf95786ae1461418498f0f32.42839246fcebd5e3f45ccd7b1cdebad7"
        # crm = self.env['crm.lead'].search([('id','=',self.id)],limit=1)
        # data = { "nombre": str(self.user_id.partner_id.name),
        #         "apellido_paterno":str(self.ap_paterno),          
        #         "apellido_materno":str(self.ap_materno),
        #         "rfc" : str(self.rfc),
        #         "importe":str(self.expected_revenue),
        #         "banco": str(self.banco),
        #         "entidad_federativa":str(self.entidad_federativa),
        #         "municipio":"Miguel Hidalgo",
        #         "asesor_id":"4994884000000419919"
        #         }
        # try:
        #     payload = json.dumps(data)
        #     headers = {
        #     'zapikey': '1003.cc7584ca319e65e957f32ce61e2f1502.fbabf6196572fa59f4c3fc203c967318',
        #     'Content-Type': 'application/json'
        #     }

        #     response=requests.request("POST", url, headers=headers, data=payload)
        #     logger.info(response.text)

        #     archivo=response.text.pdf
        #     crm.sudo().write({'archivo_base64':archivo})
        #     logger.info(response.text)
        
        # except Exception as err:
        #     raise UserError(err)        


