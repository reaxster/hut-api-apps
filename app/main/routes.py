import math

from app.main import bp
from flask import render_template, request,redirect,url_for
from app.models.api_config import APIConfig,APITimer
from app.extensions import db, hut_api
from app.lib.util.helpers import getUUID,  getOSType
import time as t


@bp.route('/')
def index():
    cnf = APIConfig.query.get(1)#APIConfig.query.all()
    time = APITimer.query.get(1)#TODO: Handle Non Existent

    if hut_api.get_is_init():
        status = hut_api.status()
    else:
        status = "unknown"


    modes = ['N/A','VTE', 'DIR','NET']
    systems = ["N/A", 'Windows', 'Ubuntu/Debian']
    auth_methods = ['None', 'HutRemote']
    moreSettings = {
        'os':getOSType(),
        'uuid':getUUID()
    }
    return render_template('index.html', api_status=status,auth_methods=auth_methods, config=cnf,modes=modes,systems=systems, d=moreSettings,num=math.floor(t.time()))#-float(time.time)

@bp.route('/timer')
def timer():
    return render_template('timer.html',num=25*60)





@bp.route('/', methods=['POST'])
def save_config():
    settings = APIConfig().query.delete()
    time = APITimer.query.delete()
    db.session.commit()

    time = APITimer(
        time=t.time()#datetime.utcnow()
    )

    settings = APIConfig(
        mode=request.form.get('mode'),
        server=request.form.get('serverUrl'),
        url_prefix=request.form.get('url_prefix'),
        token=request.form.get('token'),
        database=request.form.get('database'),
        os=request.form.get('os'),
        auth_method=request.form.get('auth_method'),
    )
    db.session.add(time)
    db.session.add(settings)
    db.session.commit()

    return redirect(url_for('main.index'))

@bp.route('/stop-start-api', methods=['GET'])
def stop_api():
    status = hut_api.status()
    if status == 'stopped':
        hut_api.start()
    else:
        hut_api.stop()

    return redirect(url_for('main.index'))
