import requests
import json
from acitoolkit.acisession import Session
from acitoolkit.acitoolkit import Credentials, Tenant, AppProfile, EPG
from acitoolkit.acitoolkit import Context, BridgeDomain, Contract, FilterEntry

#THIS CODE CAN BE USE AS BACK END CODE TO CREATE A WEB PAGE FOR ACI CONFIGURATION


base_url = '*****'        #url APIC
uri_login = base_url + 'aaaLogin.json'         #url login
uri_ctenant = base_url + 'node/mo/uni.json'


class AciCreator:

    def __init__(self,uri_login,uri_ctenant,username,password,tname,appname):
        self.uri_login = uri_login
        self.uri_ctenant = uri_ctenant
        self.username = username
        self.password = password
        self.tname = tname
        self.appname = appname

    def login(self):

        headers = {"Content-Type": "application/json","Accept":"application/json"}
        body = {"aaaUser": {"attributes": {"name": self.username,"pwd": self.password}}}

        r = requests.post(self.uri_login, json=body, headers=headers, verify=False)

        r_json = r.json()

        if r.status_code == 200:
            self.token = r_json['imdata'][0]['aaaLogin']['attributes']['token']

        if r.ok:
            print('Login successful !')

        if not r.ok:
            print("Error: Could not login to APIC")

##### CREATTION OF TENANT #####

    def ctenant(self):

        body = {"fvTenant": {"attributes": {"dn": "uni/tn-"+self.tname+"","name": self.tname,"rn": "tn-"+self.tname+"","status": "created"},"children":[]}}
        cookies =  {'APIC-Cookie': self.token}

        r = requests.post(self.uri_ctenant, json=body, cookies=cookies, verify=False )


        if r.ok:
            print('Tenant created successfully!!')
        else:
            print("Error: Could not post tenant to APIC")
            print(r.text)
        return r

##### CREATION OF APPLICATION PROFILE #####

    def cAppp(self):

        uri_cAppp = base_url + 'node/mo/uni/tn-'+self.tname+'/ap-'+self.appname+'.json'


        body = {"fvAp":{"attributes":{"dn":"uni/tn-"+self.tname+"/ap-"+self.appname+"","name":self.appname,"rn":"ap-"+self.appname+"","status":"created"},"children":[]}}
        headers = {"content-type": "application/json","Cookie": "APIC-Cookie="+ self.token}

        r = requests.post(uri_cAppp, json=body,headers=headers, verify=False )

        if r.ok:
            print('Application Profile created successfully!!')
        else:
            print("Error: Could not post application profile to APIC")
            print(r.text)

##### CREATION OF EPG AND THEIR CONTRACTS #####

    def wta_contract(self):

        uri_contract = base_url + "node/mo/uni.json"

        body = {'fvTenant': {'attributes': {'name': self.tname}, 'children': [{'fvAp': {'attributes': {'name': self.appname}, 'children': [{'fvAEPg': {'attributes': {'name': 'WEB','pcEnfPref': 'enforced'}, 'children': [{'fvRsProv': {'attributes': {'tnVzBrCPName': 'web-to-app'}}},{"fvRsDomAtt":{"attributes":{"annotation":"","bindingType":"none","classPref":"encap","customEpgName":"","delimiter":"","dn":"uni/tn-"+self.tname+"/ap-"+self.appname+"/epg-WEB/rsdomAtt-[uni/vmmp-VMware/dom-vCenter-ACI]","encap":"unknown","encapMode":"auto","epgCos":"Cos0","epgCosPref":"disabled","instrImedcy":"lazy","lagPolicyName":"","netflowDir":"both","netflowPref":"disabled","numPorts":"0","portAllocation":"none","primaryEncap":"unknown","primaryEncapInner":"unknown","resImedcy":"pre-provision","secondaryEncapInner":"unknown","switchingMode":"native","tDn":"uni/vmmp-VMware/dom-vCenter-ACI","untagged":"no"}}} ,{'fvRsBd': {'attributes': {'tnFvBDName': self.tname}}}]}},{'fvAEPg': {'attributes': {'name': 'APP'}, 'children': [{'fvRsCons': {'attributes': {'tnVzBrCPName': 'web-to-app'}}}, {'fvRsBd': {'attributes': {'tnFvBDName': self.tname}}}]}}]}}, {'fvCtx': {'attributes': {'name': 'VRF-1', 'pcEnfPref': 'enforced'}, 'children': []}}, {'fvBD': {'attributes': {'name': self.tname, 'unkMacUcastAct': 'proxy', 'unkMcastAct': 'flood', 'arpFlood': 'no', 'unicastRoute': 'yes', 'multiDstPktAct': 'bd-flood'}, 'children': [{'fvRsCtx': {'attributes': {'tnFvCtxName': 'VRF-1'}}}]}}, {'vzBrCP': {'attributes': {'name': 'web-to-app', 'scope': 'context'}, 'children': [{'vzSubj': {'attributes': {'name': 'web-to-app_Subject'}, 'children': [{'vzRsSubjFiltAtt': {'attributes': {'tnVzFilterName': 'APP'}}}]}}]}}, {'vzFilter': {'attributes': {'name': 'APP'}, 'children': [{'vzEntry': {'attributes': {'name': 'APP', 'applyToFrag': 'no', 'arpOpc': 'unspecified', 'dFromPort': '443', 'dToPort': '443', 'etherT': 'ip', 'prot': 'tcp', 'sFromPort': '1', 'sToPort': '65535', 'tcpRules': 'unspecified', 'stateful': '0'}, 'children': []}}]}}]}}

        headers = {"content-type": "application/json","Cookie": "APIC-Cookie="+ self.token}

        r = requests.post(uri_contract, json=body, headers=headers,verify=False)

        if r.ok:
            print('Web to app contract was created successfully!!')
        else:
            print("Error: Could not create contract ")
            print(r.text)


    def atd_contract(self):

        uri_contract = base_url + "node/mo/uni.json"

        body = {'fvTenant': {'attributes': {'name': self.tname}, 'children': [{'fvAp': {'attributes': {'name': self.appname}, 'children': [{'fvAEPg': {'attributes': {'name': 'DATA', 'pcEnfPref': 'enforced'}, 'children': [{'fvRsProv': {'attributes': {'tnVzBrCPName': 'app-to-data'}}},{"fvRsDomAtt":{"attributes":{"annotation":"","bindingType":"none","classPref":"encap","customEpgName":"","delimiter":"","dn":"uni/tn-"+self.tname+"/ap-"+self.appname+"/epg-DATA/rsdomAtt-[uni/vmmp-VMware/dom-vCenter-ACI]","encap":"unknown","encapMode":"auto","epgCos":"Cos0","epgCosPref":"disabled","instrImedcy":"lazy","lagPolicyName":"","netflowDir":"both","netflowPref":"disabled","numPorts":"0","portAllocation":"none","primaryEncap":"unknown","primaryEncapInner":"unknown","resImedcy":"pre-provision","secondaryEncapInner":"unknown","switchingMode":"native","tDn":"uni/vmmp-VMware/dom-vCenter-ACI","untagged":"no"}}}, {'fvRsBd': {'attributes': {'tnFvBDName': self.tname}}}]}},{'fvAEPg': {'attributes': {'name': 'APP'}, 'children': [{'fvRsCons': {'attributes': {'tnVzBrCPName': 'app-to-data'}}}, {"fvRsDomAtt":{"attributes":{"annotation":"","bindingType":"none","classPref":"encap","customEpgName":"","delimiter":"","dn":"uni/tn-"+self.tname+"/ap-"+self.appname+"/epg-APP/rsdomAtt-[uni/vmmp-VMware/dom-vCenter-ACI]","encap":"unknown","encapMode":"auto","epgCos":"Cos0","epgCosPref":"disabled","instrImedcy":"lazy","lagPolicyName":"","netflowDir":"both","netflowPref":"disabled","numPorts":"0","portAllocation":"none","primaryEncap":"unknown","primaryEncapInner":"unknown","resImedcy":"pre-provision","secondaryEncapInner":"unknown","switchingMode":"native","tDn":"uni/vmmp-VMware/dom-vCenter-ACI","untagged":"no"}}},{'fvRsBd': {'attributes': {'tnFvBDName': self.tname}}}]}}]}}, {'fvCtx': {'attributes': {'name': 'VRF-1', 'pcEnfPref': 'enforced'}, 'children': []}}, {'fvBD': {'attributes': {'name': self.tname, 'unkMacUcastAct': 'proxy', 'unkMcastAct': 'flood', 'arpFlood': 'no', 'unicastRoute': 'yes', 'multiDstPktAct': 'bd-flood'}, 'children': [{'fvRsCtx': {'attributes': {'tnFvCtxName': 'VRF-1'}}}]}}, {'vzBrCP': {'attributes': {'name': 'app-to-data', 'scope': 'context'}, 'children': [{'vzSubj': {'attributes': {'name': 'app-to-data_Subject'}, 'children': [{'vzRsSubjFiltAtt': {'attributes': {'tnVzFilterName': 'SQL'}}}]}}]}}, {'vzFilter': {'attributes': {'name': 'SQL'}, 'children': [{'vzEntry': {'attributes': {'name': 'SQL', 'applyToFrag': 'no', 'arpOpc': 'unspecified', 'dFromPort': '1433', 'dToPort': '1433', 'etherT': 'ip', 'prot': 'tcp', 'sFromPort': '1', 'sToPort': '65535', 'tcpRules': 'unspecified', 'stateful': '0'}, 'children': []}}]}}]}}

        headers = {"content-type": "application/json","Cookie": "APIC-Cookie="+ self.token}

        r = requests.post(uri_contract, json=body, headers=headers,verify=False)

        if r.ok:
            print('app to data contract was created successfully!!')
        else:
            print("Error: Could not create contract ")
            print(r.text)

##### ERASE TENANT #####


    def Tenanteraser(self):

        body = {"fvTenant" : {"attributes" : {"name" : self.tname,"status" : "deleted"}}}
        cookies =  {'APIC-Cookie': self.token}

        r = requests.post(self.uri_ctenant, json=body, cookies=cookies, verify=False )

        if r.ok:
            print('Tenant was deleted successfully!!')
        else:
            print("Error: Could not delete tenant from APIC")
            print(r.text)


api = AciCreator(uri_login,uri_ctenant,"*your username here*","*your password here*","*name of tenant here*","*name of application profile here*")
api.login()
api.ctenant()
api.cAppp()
api.wta_contract()
api.atd_contract()
#api.Tenanteraser()
