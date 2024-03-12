from app.login import bp
import jwt
from flask import session, current_app
from datetime import datetime,timedelta
from flask import render_template, request,redirect,url_for
from app.models.api_config import APIConfig
import requests
from jwt.algorithms import get_default_algorithms

@bp.route('/login', methods=['GET'])
def index():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login_submitted():
    # TODO: Do not run if Falsk Auth Not needed
    #Check for initial Configuration
    cnf = APIConfig.query.get(1)
    print(cnf)


    try:
        # If auth Method Not Defined or os None
        if not cnf or not cnf.auth_method or cnf.auth_method == 'None':
            print("Logging as None")
            token = encode_token('default')

        elif (cnf.auth_method == 'HutRemote'):
            print("Logging as HutRemote")
            #request.form['username'] and request.form['password'] == 'admin'
            # TODO: Forward Credentials to HUT URL
            #
            print(f"USERNAME: {request.form['username']}")
            print(f"PASSWORD: {request.form['password']}")
            print({'username': request.form['username'], 'password':request.form['username'], 'tenantApiDb':cnf.database})
            api_token = requests.post(
                url=f'{cnf.server}/auth/login/user-api-auth',
                data={'username': request.form['username'], 'password':request.form['password'], 'tenantApiDb':"global_tenant"}
            )
            if api_token.status_code > 400 and api_token.status_code < 500:
                raise Exception("Invalid Credentials. Status 404")
            elif api_token.status_code >= 500:
                raise Exception("There is a server error.")
            decoded = jwt.decode(api_token.json()['token'], algorithms=get_default_algorithms(), options={"verify_signature": False})
            token = encode_token(decoded['email'])

        else:
            print("REPONSE NOT VALUD")
            return render_template('login.html', msg="Invalid Credentials")

        session['logged_in'] = True
        session['token'] = token
        return redirect(url_for('main.index'))

    except Exception as e:
        print(e)
        print("REPONSE NOT VALUD - EXCEPTION")
        return render_template('login.html',msg=str(e))


@bp.route('/logout')
def logout():
    session['logged_in'] = False
    session['token'] = None
    return render_template('login.html',msg="Logged Out")



def encode_token(user):
    return jwt.encode({
        'user': user,
        'expiration': str(datetime.utcnow() + timedelta(seconds=600))
    }, current_app.config["SECRET_KEY"], algorithm="HS256")