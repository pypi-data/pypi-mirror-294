from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EstadoEnum(str, Enum):
	en_progreso = 'EN_PROGRESO'
	completada = 'COMPLETADA'
	fallo = 'FALLO'
	pendiente = 'PENDIENTE'
	string_vacio = ''


class InformacionExtraDescargaEnum(str, Enum):
	web_scraping_rues = 'web_scraping_rues'
	web_scraping_judicial = 'web_scraping_judicial'
	web_scraping_bdme = 'web_scraping_bdme'
	web_scraping_financiero = 'web_scraping_financiero'
	limpieza_de_datos = 'limpieza_de_datos'
	correr_modelo = 'correr_modelo'
	consolidar_resultados = 'consolidar_resultados'
	string_vacio = ''


class EstadoEmpresaDescarga(BaseModel):
	uuid_usuario: str
	nit: int
	fecha_compra: str
	uuid_descarga: str
	correo_usuario: str
	nombre_usuario: str
	estado_descarga: str
	informacion_extra_descarga: Optional[InformacionExtraDescargaEnum] = ''
	descripcion_error: Optional[str] = ''
	estado: Optional[EstadoEnum] = ''


class EmpresasAdquiridas(EstadoEmpresaDescarga):
	uuid_usuario_descarga_original: str
	creado_en: Optional[datetime] = None
