import nmap
from mac_vendor_lookup import MacLookup

class NMAP_Custom:

    def __init__(self):
        self.nm = nmap.PortScanner()

        #Updating MAC Vendors
        self.mac = MacLookup()
        self.mac.update_vendors()  # <- This can take a few seconds for the download


    def __prepare_manual_scan_result__(self, result: nmap.PortScanner(),network_address_id:str,networkAddress: str,) -> dict:
        ip_list = list(result['scan'])
        ip_list.sort()
        final_list = []

        for ip in ip_list:
            formatted = {}

            name_and_type = result['scan'][ip].get('hostnames')[0]

            formatted["networkID"] = network_address_id

            try:
                formatted['mac'] = result['scan'][ip]['addresses']['mac']
            except:
                formatted['mac'] = ""

            try:
                formatted['ipv4'] = result['scan'][ip]['addresses']['ipv4']
            except:
                formatted['ipv4'] = ""

            try:
                my_vendor = self.mac.lookup(result['scan'][ip]['addresses']['mac'])
                if my_vendor:
                    formatted['vendor'] = my_vendor
                else:
                    formatted['vendor'] = result['scan'][ip]['vendor'][result['scan'][ip]['addresses']['mac']]
            except:
                formatted['vendor'] = "N/A"

            try:
                formatted['hostname'] = name_and_type['name']
            except:
                formatted['hostname'] = "N/A"

            try:
                formatted['type'] = name_and_type['type']
            except:
                formatted['type'] = "N/A"


            final_list.append(formatted)
        return final_list

    def run_manual_scan(self, segment: str, network_address_id:str) -> dict:
        scan_query = self.nm.scan(hosts=segment, arguments='-n -sn')
        return self.__prepare_manual_scan_result__(scan_query,network_address_id,segment)

    def __err_handling__(func):
        try:
            result = func()
            return result
        except:
            return ""

