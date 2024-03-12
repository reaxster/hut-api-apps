import requests
import json

class HTTP:

    def __init__(self, base_url, prefix,mode, uuid, token, db):
        self.base_url = base_url
        self.url_path = prefix
        self.prefix = prefix
        self.uuid = uuid
        self.token = token
        self.db = db
        self.task_url = f"{base_url}/{prefix}/{mode}"



    def getAndParse(self, url):
        '''
        :param url is the URI to be fetched
        :return parsed data if req is successful
        '''
        print(" >> Getting Data")
        response_api = requests.get(url)
        if(response_api.status_code >= 400 ):
            raise Exception(f"Request failed with status: {response_api.status_code}. URL: {response_api.url}")
        data = response_api.text
        print(data)
        parse_json = json.loads(data)
        return parse_json

    def postAndFeedback(self, url, data):
        '''
        :param url is the URI to be fetched
        :param data is the payload to be posted
        :return parsed data if req is successful
        '''

        print(" >> Posting Data")
        response_API = requests.post(url, json=data)  # json.dumps(data)
        # extracting response text
        pastebin_url = response_API.text
        print(" >> Server Responded With: %s" % pastebin_url)
    def getAPIConfig(self):
        url = f'{self.base_url}/{self.prefix}/{self.db}/{self.uuid}/{self.token}'
        return self.getAndParse(url)


    #TODO: NETWORK CLIENT
    def restPOSTNet(self, data):
        url = f'{self.task_url}/{self.db}/{self.uuid}/{self.token}'
        self.postAndFeedback(url,data)
        pass

    def restGETNet(self):
        url = f'{self.task_url}/{self.db}/{self.uuid}/{self.token}'
        res = self.getAndParse(url)
        return res


    #TODO: VTECH CLIENT
    def restPOSTVte(self):
        '''
        Post VTech results, along with any errors that occurred during processing
        :return all VTech devices in DB
        '''
        pass

    def restGETVte(self):
        '''
        Gets all VTech device that are in DB for processing
        :return all vtech devices in DB
        '''
        pass


    #TODO: VTECH CLIENT
    def restPOSTDir(self):
        
        pass

    def restGETDir(self):
        pass
