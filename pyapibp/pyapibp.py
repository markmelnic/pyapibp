import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.basicConfig(level=logging.ERROR, format='%(message)s')

import os, uuid, shutil
from PyInquirer import prompt

from ._style import STYLE
from ._questions import *

class pyapibp:
    def __init__(self, test_mode=False) -> None:
        logging.info(f'Welcome to the Python boilerplate code generator for API\'s')

        _base_cwd = os.getcwd()
        self._flask_d = os.path.join(_base_cwd, 'pyapibp/_flask')

        self.existing = prompt(FOLDER, style=STYLE)['existing']
        if self.existing:
            logging.info(f'Make sure to navigate to it')
            self.answers = prompt(GENERAL[1:], style=STYLE)
        else:
            self.answers = prompt(GENERAL, style=STYLE)

        if not self.existing:
            os.makedirs(self.answers['title'])
        os.chdir(self.answers['title'])

        if self.answers['framework'] == 'flask':
            self._flask_bp()
        elif self.answers['framework'] == 'fastapi':
            raise NotImplementedError('FastAPI is not yet implemented')

        os.chdir(_base_cwd)
        if test_mode:
            shutil.rmtree(self.answers['title'])

    def _flask_bp(self) -> None:
        logging.info(f'Using Flask Blueprint')

        answers = prompt(FLASK, style=STYLE)

        cwd = os.getcwd()
        app_cwd = os.path.join(cwd, 'app')
        os.makedirs(app_cwd)

        with open(os.path.join(cwd, '.env'), 'w') as f:
            f.write(f'SECRET_KEY = {uuid.uuid4().hex}\nDATABASE_URL = sqlite:///.db')
        shutil.copy(os.path.join(self._flask_d, 'wsgi.py'), cwd)

        if 'Database' in answers['options']:
            shutil.copy(os.path.join(self._flask_d, '__init__.py'), app_cwd)
            shutil.copy(os.path.join(self._flask_d, 'routes.py'), app_cwd)
            shutil.copy(os.path.join(self._flask_d, 'models.py'), app_cwd)

            # os.rename(os.path.join(app_cwd, '__init__db.py'), os.path.join(app_cwd, '__init__.py'))
            # os.rename(os.path.join(app_cwd, 'routes_db.py'), os.path.join(app_cwd, 'routes.py'))
        else:
            shutil.copy(os.path.join(self._flask_d, '__init__nodb.py'), app_cwd)
            shutil.copy(os.path.join(self._flask_d, 'routes_nodb.py'), app_cwd)

            os.rename(os.path.join(app_cwd, '__init__nodb.py'), os.path.join(app_cwd, '__init__.py'))
            os.rename(os.path.join(app_cwd, 'routes_nodb.py'), os.path.join(app_cwd, 'routes.py'))

        if 'Forms' in answers['options']:
            shutil.copy(os.path.join(self._flask_d, 'forms.py'), app_cwd)

        if 'Templates Folder' in answers['options']:
            os.makedirs(os.path.join(cwd, 'app/templates'))

        if 'Static Folder' in answers['options']:
            os.makedirs(os.path.join(cwd, 'app/static'))
            os.makedirs(os.path.join(cwd, 'app/static/css'))
            os.makedirs(os.path.join(cwd, 'app/static/img'))
            os.makedirs(os.path.join(cwd, 'app/static/js'))
