# use to change localhost IP configure
# if current IP configure is DHCP,then change it to LAN IP with
#     IPADDR1:192.168.63.37
#     IPADDR2:10.114.63.37
#     NETMASK:255.255.255.0
#     GATEWAY:192.168.63.160
#     DNS:202.114.0.242
# else change IP configure to DHCP

import wmi

print "changing IP configure,wating..."

wmiService = wmi.WMI()
adapterConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)

# for adapterConfig in adapterConfigs:
    # print adapterConfig.Index
    # print adapterConfig.SettingID
    # print adapterConfig.Description
    # print adapterConfig.IPAddress
    # print adapterConfig.IPSubnet
    # print adapterConfig.DefaultIPGateway
    # print adapterConfig.DNSServerSearchOrder
#print adapterConfigs[0].IPAddress[0]

if len(adapterConfigs) < 1:
    print "oops..not found any adapters.."
    print "exit.."
    exit()
    
#localhost Adapter always with index 0
localhostConfig = adapterConfigs[0]
if localhostConfig.IPAddress[0] == "192.168.63.37":
    print "current IP configure is static,change to DHCP."
    #try:
    localhostConfig.SetDNSServerSearchOrder()
    localhostConfig.EnableDHCP()
    #except BaseException, e:
    #    print (str(e))
    #	exit()
    print "Done. ^_^"
else:
    print """current IP configure is DHCP,change to configure with:
                IPADDR1:192.168.63.37
                IPADDR2:10.114.63.37
                NETMASK:255.255.255.0
                GATEWAY:192.168.63.160
                DNS:202.114.0.242"""
    
    ipAddrs = ["192.168.63.37"]
    netmask = ["255.255.255.0"]
    gateway = ["192.168.63.160"]
    metrics = [1]
    dnsServ = ["202.114.0.242","8.8.8.8"]
    intreboot = 0
    
    #setting static IP address.
    ret = localhostConfig.EnableStatic(IPAddress = ipAddrs, SubnetMask = netmask)
    #for res in ret:
    #    print res
    if ret[0] == 0:
        print "setting IP addrs success."
    elif ret[0] == 1:
    	print "setting IP addrs success."
        intreboot += 1
    else:
        print "configure IP address error!!"
        exit()
    
    #setting gateway
    ret = localhostConfig.SetGateways(DefaultIPGateway = gateway, GatewayCostMetric = metrics)
    if ret[0] == 0:
        print "setting gateway success."
    elif ret[0] == 1:
        print "setting gateway success."
        intreboot += 1
    else:
        print "configure gateway error!"
        exit()
    
    #setting DNS servers
    ret = localhostConfig.SetDNSServerSearchOrder(DNSServerSearchOrder = dnsServ)
    if ret[0] == 0:
        print "setting DNS success."
    elif ret[0] == 1:
        print "setting DNS success."
        intreboot += 1
    else:
        print "configure DNS error!"
        exit()
    
    #done..
    if intreboot > 0:
        print "need to reboot.."
    else:
        print "Done. ^_^"
