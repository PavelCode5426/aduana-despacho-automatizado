from configparser import ConfigParser

config_object = ConfigParser()


def init_config():
    readed = config_object.read('config.ini')
    if not len(readed):
        config_object.add_section('SERVER')
        config_object.set('SERVER', 'HOST', 'http://127.0.0.1:8000')
        config_object.set('SERVER', 'ENDPOINT', 'api/aduana/request-bulletin')
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
