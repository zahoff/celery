import os 

from flask import Flask, jsonify, send_file, request
from flask.views import MethodView
from celery.result import AsyncResult

from upscale_task import celery, upscale


app_name = 'upscaling'
app = Flask(app_name)
app.config['UPLOAD_FOLDER'] = 'results'


celery.conf.update(app.config)


class Upscaling(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        if task.status == 'PENDING':
            return jsonify({'status': task.status, 
                            'link': 'link is not ready yet'})
        elif task.status == 'SUCCESS':
            return jsonify({'status': task.status, 
                            'link': f'http://127.0.0.1:5000/processed/{request.json["filename"]}'})
    
    def post(self):
        task = upscale.delay(input_path=request.json['input_path'], 
                             output_path=request.json['output_path'])
        return jsonify({'task_id': task.id})


class Upscaled(MethodView):
    
    def get(self, filename):
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file, mimetype='image/gif') 


upscaling_view = Upscaling.as_view('upscaling')
upscaled_view = Upscaled.as_view('upscaled')
app.add_url_rule('/upscale', view_func=upscaling_view, methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=upscaling_view, methods=['GET'])
app.add_url_rule('/processed/<filename>', view_func=upscaled_view, methods=['GET'])


if __name__ == '__main__':
    app.run()