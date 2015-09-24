import ConfigParser

config = ConfigParser.RawConfigParser()

config.add_section('Buttons')
config.set('Buttons', 'time_1', '45 minutes')
config.set('Buttons', 'time_2', '1 Hour')
config.set('Buttons', 'time_3', '2 Hours')
config.set('Buttons', 'time_4', '3 Hours')
config.add_section('Times')
config.set('Times', 'time_1', '45')
config.set('Times', 'time_2', '60')
config.set('Times', 'time_3', '120')
config.set('Times', 'time_4', '180')
config.add_section('Install_Dir')
config.set('Install_Dir','dir','C:\Program Files\HTC Logoff')

with open('test_config.cfg', 'wb') as configfile:
    config.write(configfile)
    
