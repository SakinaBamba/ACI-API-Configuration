from acitoolkit.acisession import Session
from acitoolkit.acitoolkit import Credentials, Tenant, AppProfile, EPG, EPGDomain,VmmDomain,CommonEPG
from acitoolkit.acitoolkit import Context, BridgeDomain, Contract, FilterEntry

def main():

    description = ('Create 3 EPGs within the same Bridge Domain and have'
                   '2 EPGs provide a contract to the other EPG.')
    creds = Credentials('apic', description)
    args = creds.get()




    # Login to APIC and push the config
    session = Session(args.url, args.login, args.password,verify_ssl = False)
    log = session.login()

    if log.ok:
        print('Login to APIC successful !!!')

    if not log.ok:
        print('Error: Could not login to APIC')
        print(log.status_code)




    # Create the Tenant
    name_tenant = input('Enter Tenant name: ')
    tenant = Tenant(name_tenant)
    tenant_resp = tenant.push_to_apic(session)

    if tenant_resp.ok:
        print('Tenant created successfully !!!')

    if not tenant_resp.ok:
        print('Error: Could not create Tenant')
        print(tenant_resp.status_code)




    # Gets vmm domain from APIC
    vmm = VmmDomain.get_by_name(session,'vCenter-ACI')
    vmm_resp = tenant.push_to_apic(session)

    if vmm_resp.ok:
        print('VmmDomain: vCenter-ACI, opened successfully !!!')

    if not vmm_resp.ok:
        print('Error: Could not open VmmDomain: vCenter-ACI')
        print(vmm_resp.status_code)




    # Create the Application Profile
    name_ap = input('Enter Application Profile name: ')
    app = AppProfile(name_ap, tenant)
    app_resp = tenant.push_to_apic(session)


    if app_resp.ok:
        print('Application Profile created successfully !!!')

    if not app_resp.ok:
        print('Error: Could not create Application Profile')
        print(app_resp.status_code)




    # Create the WEB EPG
    web_epg = EPG('WEB', app)
    web_resp = tenant.push_to_apic(session)

    if web_resp.ok:
        print('WEB epg created successfully !!!')

    if not web_resp.ok:
        print('Error: Could not create WEB epg')
        print(web_resp.status_code)



    # Create the DATA EPG
    db_epg = EPG('DATA', app)
    db_resp = tenant.push_to_apic(session)

    if db_resp.ok:
        print('DATA epg created successfully !!!')

    if not db_resp.ok:
        print('Error: Could not create DATA epg')
        print(db_epg.status_code)



    # Create the APP EPG
    app_epg = EPG('APP', app)
    app_resp = tenant.push_to_apic(session)

    if app_resp.ok:
        print('APP epg created successfully !!!')

    if not app_resp.ok:
        print('Error: Could not create APP epg')
        print(app_epg.status_code)




    # Associating EPGs to Vmm Domain
    web_epg.attach(vmm)
    db_epg.attach(vmm)
    app_epg.attach(vmm)



    # Create a Context and BridgeDomain
    # Place both EPGs in the Context and in the same BD
    bd = BridgeDomain('BD-1', tenant)
    web_epg.add_bd(bd)
    db_epg.add_bd(bd)
    app_epg.add_bd(bd)



    # Define web-to app contract
    contract1 = Contract('web-to-app', tenant)
    entry1 = FilterEntry('entry1',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='443',
                         dToPort='443',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=contract1)


    # Define app-to-data contract
    contract2 = Contract('app-to-data', tenant)

    entry2 = FilterEntry('entry2',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='1433',
                         dToPort='1433',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=contract2)


    # Provide the contract from 1 EPG and consume from the other
    db_epg.provide(contract2)
    web_epg.provide(contract1)
    app_epg.consume(contract1)
    app_epg.consume(contract2)


########### ClEANUP (uncomment the next line to delete the tenant)
    #tenant.mark_as_deleted()
####################################

    #Push all the config to apic
    resp = tenant.push_to_apic(session)

    if resp.ok:
        print('All the configuration was pushed to APIC !!!')

    if not resp.ok:
        print('Error: Could not push configuration to APIC')
        print(resp.status_code)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
