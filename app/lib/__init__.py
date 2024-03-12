from configparser import ConfigParser
import sys
from app.lib.apiNetwork import NetworkAPI
from app.lib.apiVtech import vtechAPI
from app.lib.apiDirectory import directoryAPI
from threading import Thread
from datetime import datetime, timedelta




class Hut_Api():
    def __init__(self):
        self.APIConfig = None
        self.APITimer = None
        self.job = None
        self.app = None
        self.db = None
        self.is_init = False



    def init_app(self, db, APIConfig, APITimer):#
        self.APIConfig = APIConfig
        self.APITimer = APITimer
        self.db = db

        config = APIConfig.query.get(1)

        if not config:
            raise Exception("The configuration is missing. Please configure the database")

        self.job = Thread()
        try:
            mode = config.mode

            if str(mode).lower() == "net":
                self.app = NetworkAPI(config, self.__set_run_every__)
                pass
            elif str(mode).lower() == "vte":
                # self.app = vtechAPI.VtechAPI(config,  self.__set_run_every__)
                pass
            elif str(mode).lower() == "dir":
                # self.app = directoryAPI.DirectoryAPI(config, self.__set_run_every__)
                pass
            else:
                raise Exception("No mode has been provided in config.ini.\nValid modes are NET | DIR | VTE")
        except Exception as e:
            print("AN UNKNOWN EXCEPTION IN MAIN OCCURRED")
            print(e)
            return False

        self.is_init = True


    def start(self):
        try:
            if not self.is_init:
                raise Exception("The App is no initialized")
            self.job = Thread(target=self.app.start)
            self.job.daemon = True
            self.job.start()
        except Exception as e:
            print("An Error Has Occurred White Starting the App")
            print(e)
            sys.exit(1)


    def stop(self):
        try:
            if not self.is_init:
                raise Exception("The App is no initialized")
            self.app.stop()
            self.job.join()
        except Exception as e:
            print("An Error Has Occurred while stopping the App")
            print(e)




    def status(self):

        try:
            if not self.is_init:
                raise Exception("The App is no initialized")
            return self.app.status()
        except Exception as e:
            print("An Error Has Occurred While getting the status of the app")
            print(e)

    def get_is_init(self):
        return self.is_init

    def __set_run_every__(self, after_min):
        now = datetime.now()
        next_api_call = now + timedelta(minutes=after_min)
        #self.APITimer.query.delete()
        #self.db.session.add(self.APITimer(
            #time=next_api_call  # datetime.utcnow()
        #))
        #self.db.session.commit()










