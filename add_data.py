import station
import time
from datetime import datetime
from datetime import timedelta

pst2utc = timedelta(hours=7)
date = ''

while(True):
    #if(date != (datetime.utcnow()-pst2utc).day):
    date = (datetime.utcnow()-pst2utc).day
    Durand = station.name('/home/ec2-user/snowfort/snowfort-ui-master_py2/motes/Durand')
    Durand.connectToFtp('/home/ec2-user/snowfort/snowfort-ui-master_py2/key.FTP')
    Durand.addattribute('wind_direction', 2)
    Durand.addattribute('wind_speed', 3)
    
    Huang = station.name('/home/ec2-user/snowfort/snowfort-ui-master_py2/motes/Huang')
    Huang.connectToFtp('/home/ec2-user/snowfort/snowfort-ui-master_py2/key.FTP')
    Huang.addattribute('wind_direction', 2)
    Huang.addattribute('wind_speed', 3)

    try: 
        Durand.readFromFtp()
        Huang.readFromFtp()

        Durand.addToMysql()
        Huang.addToMysql()
    except Exception as e:  
        print(e)
        time.sleep(1)
        continue