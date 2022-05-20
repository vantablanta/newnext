from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_share import Share

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

photos = UploadSet('photos',IMAGES)


db = SQLAlchemy()
from .models import Users

share = Share()



def create_app(config_name):
    app = Flask(__name__)
    
    from config import config_options
    app.config.from_object(config_options[config_name])
    app.config['UPLOADED_PHOTOS_DEST']='app/static/images/uploads'
    app.config['ALLOWED_EXTENSIONS']='{png', 'jpg', 'jpeg}'
    
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    configure_uploads(app,photos)

    share.init_app(app)


    return app


