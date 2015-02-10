import ConfigParser

config = ConfigParser.RawConfigParser()

config.add_section('Buttons')
config.set('Buttons', 'time_1', 'button1')
config.set('Buttons', 'time_2', 'button2')
config.set('Buttons', 'time_3', 'button3')
config.set('Buttons', 'time_4', 'button4')

with open('logoff_config.cfg', 'wb') as configfile:
    config.write(configfile)
    
