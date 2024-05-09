import json
import logging


def extract_message_id(event):
    """
    Extrae el identificador del mensaje y el asunto del correo electrónico a partir de un evento SNS de AWS.

    Esta función está diseñada para ser utilizada con eventos que provienen de notificaciones Amazon SNS, 
    especialmente aquellos relacionados con Amazon SES (Simple Email Service). El objetivo es extraer el 
    identificador del mensaje y el asunto del correo electrónico del contenido del mensaje SNS.

    Args:
        event (dict): Evento AWS, generalmente originado por una notificación SNS relacionada con SES.

    Returns:
        tuple:
            message_id (str): Identificador único del mensaje de correo electrónico.
            subject (str): Asunto del correo electrónico. Puede retornar None si el asunto no está presente.

    Raises:
        KeyError, TypeError, IndexError: Si el evento no tiene la estructura esperada.
        json.JSONDecodeError: Si el contenido del mensaje no puede ser decodificado como un JSON válido.

    Notes:
        La función espera que el evento tenga una estructura específica de notificaciones SNS relacionadas 
        con SES. Un uso con eventos de otro tipo o con una estructura diferente puede resultar en excepciones.
    """
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        message = event['Records'][0]['Sns']['Message']
    except (KeyError, TypeError, IndexError) as e:
        logger.error("No se pudo obtener el mensaje del evento: %s", e)
        raise e
    
    try:
        decoded_message = json.loads(message)
    except json.JSONDecodeError as e:
        logger.error("No se pudo decodificar el mensaje JSON: %s", e)
        raise e
    
    try:
        message_id = decoded_message['mail']['messageId']
        subject = decoded_message['mail']['commonHeaders'].get('subject', None)
   
    except KeyError as e:
        logger.error("No se pudo obtener el %s", e)
        raise e
    
    logger.info("El messageId es: %s", message_id)
    return message_id,subject