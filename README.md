Py_LogOff
=========

A logoff utility written in C# and WPF that prompts the user for how long they want to be logged in 
then logs them off after that period of time. Will not allow the user to close the appliaction 

If the user does not choose a time, this logs the user off after 1 hour

When the initial time is up, this program asks if they need 5 more minutes. They can select yes up to 3 times. If nothing is entered, this will log the user off automatically after 5 minutes.

Compiled win32 binaries can be found at:

http://livinginsyn.com/logoff_binaries/


