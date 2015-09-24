using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.AccessControl;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;

namespace HTC_LogOut
{
    public class Logger
    {

        private NameGetter namer;

        public Logger()
        {
            namer = new NameGetter();
        }

        public void start_log()
        {
            writeLog("start");
        }

        public void logAutoLogOff()
        {
            writeLog("logout");
        }

        public void logSelection(string min, string hr)
        {
            writeLog("selection", min, hr);
        }

        public void logLogoutNow()
        {
            writeLog("manual_logout");
        }

        private void writeLog(string type,string min="0",string hr="0")
        {
            string name = namer.get_userName();

            string path = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            Debug.WriteLine(path);

            //string directory = System.IO.Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            string directory = "C:\\ProgramData\\HTC-Logout";
            string logdirectory = directory + "\\logs";
            if (System.IO.Directory.Exists(logdirectory) == false)
            {
                System.IO.Directory.CreateDirectory(logdirectory);
            }

            string filePath = logdirectory + "\\logoff_log.txt";
            using (System.IO.StreamWriter file = new System.IO.StreamWriter(filePath, true))
            {
                //set the permissions
                GrantAccess(filePath);

                string dateTime = DateTime.Now.ToString(@"MM\/dd\/yyyy h\:mm tt");
                if (type == "start")
                { 
                    string toLog = dateTime + " " + name + " logged in and logout utility launched";
                    file.WriteLine(toLog);
                }
                else if (type == "selection")
                {
                    string toLog = dateTime + " " + name + " selected time of " + hr + " hour(s) and " + min + " minutes";
                    file.WriteLine(toLog);
                }
                else if (type == "logout")
                {
                    string toLog = dateTime + " " + name + " was logged out automatically";
                    file.WriteLine(toLog);
                }
                else if (type == "manual_logout")
                {
                    string toLog = dateTime + " " + name + " logged out by clicking logout now";
                    file.WriteLine(toLog);
                }
            }
        }

        private void GrantAccess(string fullPath)
        {
            DirectoryInfo dInfo = new DirectoryInfo(fullPath);
            DirectorySecurity dSecurity = dInfo.GetAccessControl();
            dSecurity.AddAccessRule(new FileSystemAccessRule(new SecurityIdentifier(WellKnownSidType.WorldSid, null), FileSystemRights.FullControl, InheritanceFlags.ObjectInherit | InheritanceFlags.ContainerInherit, PropagationFlags.NoPropagateInherit, AccessControlType.Allow));
            dInfo.SetAccessControl(dSecurity);
        }



    }
}
