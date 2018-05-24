from forms import *
from model import *
from core import oss, logger, db
from core.flask_oss import gen_filename
from helpers import CustomFlask
from flask_migrate import Migrate
import os


def create_app():
    app = CustomFlask(__name__)
    config = os.environ.get('CONFIG', 'config.DevConfig')
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)
    return app


app = create_app()


@app.route('/', method='POST')
def hello_world():
    form = UploadProjectForm()
    if form.validate():
        form.create()
        logger.debug('### form created successfully')
    return 'Hello World!'


@app.route('/upload', method='POST')
def upload():
    logger.debug('###request.method: %s, request.endpoint: %s', request.method, request.endpoint)
    logger.debug('###request.form: %s,  request.files: %s', request.form, request.files)
    file = request.form.get('file')
    type = request.form.get('type', '')
    filename = 'BP/' + gen_filename(type) + request.form.get('file')
    oss.bucket.put_object(filename, file, {'Content-Type': type})
    url = f'{oss.domain_schema}://{oss.bucket.bucket_name}.{oss.domain}/{filename}'
    # 保存到数据库
    ur = UploadRecord(
        mimetype=type,
        filename=filename, url=url
    )
    db.session.add(ur)
    db.session.commit()
    return url


if __name__ == '__main__':
    app.run()
