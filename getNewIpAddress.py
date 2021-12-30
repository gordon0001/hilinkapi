from HiLinkAPI import webui
import logging
from time import sleep, time
from datetime import datetime

logging.basicConfig(filename="hilinkapitest.log", format='%(asctime)s --  %(name)s::%(levelname)s -- {%(pathname)s:%(lineno)d} -- %(message)s', level=logging.DEBUG, datefmt="%Y-%m-%d %I:%M:%S %p:%Z")

deviceFound = False
firstFoundDeviceOnly = True
try:
    webUIArray = [
        webui("E818-26X", "192.168.8.1", "admin", "admin"), # -260 (Vodaphone?) or -263 (Drei?). Both are fully unlocked, the -263 just has a few more LTEBands to use, otherwise both are perfectly suitable for Germany and Austria 
        webui("E3372h-153", "192.168.18.1", "admin", "admin", logger=logging), # known as a reliable LTE modem over the world and works  in optionalally over ncm protocol (usb cdc ncm, fw 21.XX, nonhilink) or over ethernet (usb cdc ether, fw 22.XX, hilink) mode
        webui("E3372h-320", "192.168.8.1", "admin", "abcd@1234", logger=logging),
    ]
    for webUI in webUIArray:
        try:
            # start
            webUI.start()
            # wait until validate the session
            while not webUI.getValidSession():
                # check for active errors
                if webUI.getActiveError() is not None:
                    error = webUI.getActiveError()
                    print(error)
                    sleep(5)
                # check for login wait time
                if webUI.getLoginWaitTime() > 0:
                    print(f"Login wait time available = {webUI.getLoginWaitTime()} minutes")
                    sleep(5)
            deviceFound = True
            ########
            # Enable data roaming and set max idle time out into 2 hours (7200 seconds)
            # webUI.configureDataConnection(True, 7200)
            ########
            # query data  connection
            webUI.queryDataConnection()
            # query device info
            webUI.queryDeviceInfo()
            # query WAN IP
            webUI.queryWANIP()
            # query network name
            webUI.queryNetwork()
            ###################
            #######Call gets###
            print(f"devicename = {webUI.getDeviceName()}")
            print(f"webui version = {webUI.getWebUIVersion()}")
            print(f"login required = {webUI.getLoginRequired()}")
            print(f"valid session = {webUI.validateSession()}")
            print("########################################")
            # session refresh interval
            # webUI.setSessionRefreshInteval(10)
            print(f"Session refresh interval = {webUI.getSessionRefreshInteval()}")
            print("########################################")
            # set primary and secondary network modes
            netMode = webUI.setNetwokModes("LTE", "WCDMA")
            print(f"Network mode setting = {netMode}")
            print(webUI.getNetwokModes())
            # Device info
            print("########################################")
            deviceInfo = webUI.getDeviceInfo()
            for key in deviceInfo.keys():
                if len(key) >= 8:
                    print(f"{key}\t:{deviceInfo[key]}")
                else:
                    print(f"{key}\t\t:{deviceInfo[key]}")
            #
            print("########################################")
            print(f"Network = {webUI.getNetwork()}")
            print("########################################\n")
            ######### Reboot #########
            # webUI.reboot()
            #######Reboot end#########
            # switching LTE / WCDMA
            print(f"\t{datetime.now()}")
            webUI.queryWANIP()
            print(f"\tWAN IP = {webUI.getWANIP()}")
            status = webUI.switchNetworMode(False)
            print(f"\tSwitching - WCDMA = \t{status}")
            sleep(1)
            status = webUI.switchNetworMode(True)
            print(f"\tSwitching - LTE = \t{status}")
            webUI.queryWANIP()
            while webUI.getWANIP() is None:
                webUI.queryWANIP()
            print(f"\tWAN IP = {webUI.getWANIP()}")
            print(f"\t{datetime.now()}\n")
            print("****************************************\n\n")
            ###################
            # stop
            webUI.stop()
            while(not webUI.isStopped()):
                webUI.stop()
                print(f"Waiting for stop")
                sleep(1)
        except Exception as e:
             print(e)
        if firstFoundDeviceOnly is True and deviceFound is True:
           break
except Exception as e:
    print(e)
# End of the test
print("\n")