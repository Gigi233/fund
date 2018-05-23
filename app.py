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


@app.route('/', method='POST')
def hello_world():
    form = UploadProjectForm()
    if form.validate():
        form.create()
        logger.debug('### form created')
    return 'Hello World!'


@app.route('/upload', method='POST')
def upload(self, file):
    filename = 'BP/' + gen_filename(mimetype)
    oss.bucket.put_object(filename, file, {'Content-Type': mimetype})
    url = f'{oss.domain_schema}://{oss.bucket.bucket_name}.{oss.domain}/{filename}'
    # 保存到数据库
    ur = UploadRecord(
        mimetype=mimetype,
        filename=filename, url=url
    )
    db.session.add(ur)
    db.session.commit()
    return url


if __name__ == '__main__':
    create_app().run()
