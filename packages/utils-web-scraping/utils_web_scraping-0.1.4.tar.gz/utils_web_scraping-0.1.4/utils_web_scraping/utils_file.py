import requests

if __name__ == '__main__':
	from schemas import *
else:
	from utils_web_scraping.schemas import *


def extract_info_from_event(event: dict, download_status: str, extra_download_info: str, error_description: str, status: str) -> EstadoEmpresaDescarga:
	download_status_object = EstadoEmpresaDescarga(
		uuid_usuario=event['UID_USUARIO'],
		nit=event['NIT'],
		fecha_compra=event['fecha_descarga_sin_espacios'],
		uuid_descarga=event['UUID_FUNCION'],
		correo_usuario=event['CORREO_USUARIO'],
		nombre_usuario=event['NOMBRE_USUARIO'],
		estado_descarga=download_status,
		informacion_extra_descarga=extra_download_info,
		descripcion_error=error_description,
		estado=status)

	return download_status_object


def change_download_status(env, event: dict, download_status: str, extra_download_info: str, error_description: str, status: str)  -> bool:
	if env == 'development':
		api_endpoint = 'http://127.0.0.1:8000'
	elif env == 'staging':
		api_endpoint = 'https://k1dh50y858.execute-api.us-east-1.amazonaws.com/staging/'
	elif env == 'production':
		api_endpoint = 'https://tykeapi.com'
	else:
		raise Exception(KeyError(f"El valor para env de: {env} no se reconoce"))


	request_body = extract_info_from_event(event, download_status, extra_download_info, error_description, status)

	response = requests.post(
		f"{api_endpoint}/correr-modelo/estado-descarga",
		json=request_body.dict()

	)

	if response.status_code == 200:
		data = response.json()
		print("LA INFORMACION ES: ", data)
		return True
	else:
		print(f"Error: {response.status_code}")
		return False

