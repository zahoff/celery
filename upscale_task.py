import os 

from cachetools import cached
import cv2
from cv2 import dnn_superres
from celery import Celery 


celery = Celery(
    'upscaling',
    backend=('redis://127.0.0.1:6379/1'),
    broker=('redis://127.0.0.1:6379/2')
)

# celery = Celery(
#     'upscaling',
#     backend=os.getenv('BACKEND'),
#     broker=os.getenv('BROKER')
# )

@cached({})
def get_model(model_path: str = os.path.join('models', 'EDSR_x2.pb')):
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    return scaler 


@celery.task()
def upscale(input_path: str, output_path: str) -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """

    scaler = get_model()
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


def example():
    upscale(os.path.join('example', 'lama_300px.png'), os.path.join('results', 'lama_600px.png'))


if __name__ == '__main__':
    example()