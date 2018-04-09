from flask import render_template
from flask import jsonify

from indecision import app
from orator import DatabaseManager, Model

from json import loads
from requests import get

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'indecision',
        'user': 'arun',
        'password': 'password',
        'prefix': ''
    }
}


def load_data():
    try:
        db = DatabaseManager(config).connection()
        if not db.table('greetings').get(['message']).first():
            db.table('greetings').insert({'message': 'Hello world!'})
    except Exception as e:
        app.logger.error('Unable to connect to db: %s' % e)


def db_health(config):
    try:
        DatabaseManager(config).connection().get_connection()
        return 'Ok'
    except Exception as e:
        return 'Failure %s' % e


def instance_region():
    # INSTANCE_ID_DOC_URL = \
    #     'http://169.254.169.254/latest/dynamic/instance-identity/document'
    # return loads(get(INSTANCE_ID_DOC_URL).content)['region']
    return 'us-west-2'


def nginx_version():
    return '1.2.3'


def instance_count():
    # TODO: Implement lookup
    return 2


@app.route('/')
def index():
    load_data()
    db = DatabaseManager(config).connection()
    res = db.table('greetings').get(['message']).first()
    return render_template('index.html', message=res.get('message'))


@app.route('/health')
def health():
    return db_health(config)


@app.route('/diag')
def diag():
    return jsonify({
        'number_of_instances': instance_count(),
        'region': instance_region(),
        'health_status': db_health(config),
        'nginx_version': nginx_version()
    })
