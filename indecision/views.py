from time import time
import datetime
from json import loads

from requests import get

from flask import render_template
from flask import jsonify

from indecision import app
from orator import DatabaseManager

from .aws.s3 import s3_pull_file
from .aws.rds import get_db_config


def init_app():
    db_config = get_db_config()
    config = app.config.get('DB_CONFIG').get('mysql')
    config['user'] = db_config.get('username')
    config['password'] = db_config.get('password')
    config['host'] = db_config.get('host')
    config['database'] = db_config.get('dbname')
    config['port'] = db_config.get('port')


def load_data():
    try:
        db = DatabaseManager(app.config.get('DB_CONFIG')).connection()
        if not db.table('greetings').get(['message']).first():
            db.table('greetings').insert({'message': 'Hello world!'})
    except Exception as e:
        app.logger.error('Unable to connect to db: %s' % e)


def db_health():
    try:
        DatabaseManager(
            app.config.get('DB_CONFIG')).connection().get_connection()
        return 'Ok'
    except Exception as e:
        return 'Failure %s' % e


def instance_region():
    instance_id_doc_url = \
        'http://169.254.169.254/latest/dynamic/instance-identity/document'
    return loads(get(instance_id_doc_url).content)['region']


def nginx_version():
    return '1.2.3'


def instance_count():
    return 2


@app.route('/')
def index():
    ts = time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    db = DatabaseManager(app.config.get('DB_CONFIG')).connection()
    res = db.table('greetings').get(['message']).first()
    return render_template('index.html',
                           message=res.get('message'),
                           time=st,
                           image_to_show=app.config.get('IMAGE_DEST_PATH'))


@app.route('/health')
def health():
    return db_health()


@app.route('/diag')
def diag():
    return jsonify({
        'number_of_instances': instance_count(),
        'region': instance_region(),
        'health_status': db_health(),
        'nginx_version': nginx_version()
    })


@app.before_first_request
def initialize():
    app.logger.info('Initalizing application')
    init_app()
    app.logger.info('Loading db data')
    load_data()
    app.logger.info('Download image from s3 bucket')
    s3_pull_file(app.config.get('IMAGE_S3_BUCKET'),
                 app.config.get('IMAGE_PATH'),
                 app.config.get('IMAGE_DEST_PATH'))
