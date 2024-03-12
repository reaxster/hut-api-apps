from app.lib.util.HTTP import HTTP
from app.lib.util.UUID import getUUID
import time
from threading import Thread, active_count
from app.lib.apiNetwork.NMAP_Custom import NMAP_Custom
from app.lib.util.common import countdown
class NetworkAPI:

    def __init__(self, config,set_run_every):
        baseURL = config.server
        token = config.token
        db = config.database
        mode = str(config.mode).lower()
        #url_path = f'{config.server}/api-apps/{str(config.mode).lower()}'#config.net_url_path
        prefix = 'api-apps'
        uuid = getUUID()
        self.app_status = "stopped"
        self.http = HTTP(baseURL, prefix, mode, uuid, token, db)
        self.scan = NMAP_Custom()
        self.set_run_every=set_run_every

    def start(self):
        self.app_status = "started"
        self.__run_job__()

    def stop(self):
        self.app_status = "stopped"

    def status(self):
        return str(self.app_status)


    def __run_job__(self):
        while self.app_status == "started" or self.app_status == "running":
            self.app_status = "running"
            try:
                print(" >> Network API has been started...")
                api_config = self.http.getAPIConfig()
                networks = self.http.restGETNet()

                print(api_config)

                if not api_config:
                    raise Exception("Either the API information is missing on the server or the Database URL is incorrect or token provided is invalid")

                if len(networks) == 0:
                    print("There are not networks defined on the server. Waiting 30 sec for next attempt")
                    time.sleep(30)
                    continue

                run_every = int(api_config['run_every'])


                for network in networks:
                    thread = Thread(target=self.__processBatch__, args=(network,))
                    thread.start()
                    pass

                # WAIT 5MIN FOR NEXT API CALL
                while active_count() > 10+len(networks):
                    self.app_status = "waiting"
                    print(f" >> Waiting for other jobs: {active_count()-(10+len(networks))}")
                    time.sleep(5)
                self.set_run_every(run_every)
                countdown(run_every, f"Waiting {run_every}min for next SCAN", " To Next Scan")
                self.app_status = "started"
            except Exception as e:
                print("An Exception has Occurred in the Network Module")
                print(e)
                self.app_status = "stopped"

    def __processBatch__(self, network):
        print(f" >> NEW JOB: Scanning Network: {network['alias']} - {network['network_address']}\n")
        batch = self.scan.run_manual_scan(network['network_address'], network['_id'])
        print(batch)
        self.http.restPOSTNet(batch)
        print(f" >> JOB ENDED: Network: {network['alias']} - {network['network_address']}")
        time.sleep(2)