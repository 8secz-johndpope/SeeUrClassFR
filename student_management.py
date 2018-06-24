import io
import boto3
import re
from PIL import Image


def pars_name(text):
    regex = r'alumno_[a-z]*_[a-z]*.jpg'
    result = re.findall(regex, text)
    result_key = result[0]
    result_meta = result_key[7:-4].replace('_', ' ').title()
    return result_key, result_meta


def add_student_s3(bucket, imagenEntrada):
    s3 = boto3.client('s3')
    imagen = Image.open(imagenEntrada)
    stream = io.BytesIO()
    imagen.save(stream, format='JPEG')
    imagenCodificado = stream.getvalue()
    key, meta = pars_name(imagenEntrada)
    s3.put_object(
        Body=imagenCodificado,
        Bucket=bucket,
        ContentType='image/jpeg',
        Key=key,
        Metadata={
            'fullname': meta
        }
    )
