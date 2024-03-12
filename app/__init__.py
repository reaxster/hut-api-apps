from flask import Flask, request, jsonify, current_app,session,render_template
import jwt
from config import Config
from app.extensions import db, bcrypt,hut_api
from datetime import datetime
from app.models.api_config import APIConfig, APITimer



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)




    #TODO: Start App Here

    # Initialize Flask extensions here
    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        try:
            hut_api.init_app(db, APIConfig, APITimer)
            if hut_api.get_is_init():
                hut_api.start()
        except Exception as e:
            print(f'EXCEPTION: {str(e)}')




    #Login Middleware
    @app.before_request
    def before_request_callback():
        print("THIS S THE MIDDLEWARE")

        if(str(request.url).find("login") > 0 or str(request.url).find("static") > 0):
            return
        else:
            print(f'MIDDLWARE: {session.get("token")}')
            token = session.get('token')
            if not token:
                print("TOKEN DOESNT EXIST")
                return render_template('login.html', msg="No Token Found")
            try:
                print("TOKEN EXIST")
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                if(str(payload['expiration']) < str(datetime.utcnow())):
                    return render_template('login.html', msg="Access Token Expired")
            except Exception as e:
                print(e)
                print("EXCEPTION")
                return jsonify({"Alert": "Invalid Token!"})
        pass




    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)





    @app.route('/test/')
    #@auth_middleware
    def test_page():

        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app