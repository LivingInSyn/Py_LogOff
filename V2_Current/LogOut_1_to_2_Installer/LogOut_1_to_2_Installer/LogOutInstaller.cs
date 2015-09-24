using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Reflection;
using Microsoft.Win32;
using System.Diagnostics;

namespace LogOut_1_to_2_Installer
{
    class LogOutInstaller
    {

        private static void deleteFiles(string filePath)
        {
            // we need to add the following to ensure we can delete the file if it still exists and is running

            try
            {
                Process[] proc = Process.GetProcessesByName("HTC-LogOut");
                for(int i=0; i< proc.Length; i++)
                {
                    proc[i].Kill();
                }                
                System.Threading.Thread.Sleep(5000);
            }
            catch (Exception e)
            {
                Console.WriteLine("process not running, continuing");
            }


            string[] fileEntries = Directory.GetFiles(filePath);
            foreach (string file in fileEntries)
            {
                //Console.WriteLine(file);
                File.Delete(file);
            }
        }

        private static void copyNewFiles(string filePath)
        {

            filePath = filePath + @"\";

            File.Copy("logOutFiles\\HTC-LogOut.exe", filePath+"HTC-LogOut.exe");
            File.Copy("logOutFiles\\uninstall.exe", filePath+"uninstall.exe");
                       

        }

        private static void makeRegEntries(string dir)
        {
            
            RegistryKey startupkey = Registry.LocalMachine.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", true);

            RegistryKey uninstallkey = Registry.LocalMachine.OpenSubKey("Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall", true);

            string runDir = "\"" + dir + @"\HTC-LogOut.exe" + "\"";

            string uninstallString = "\"" + dir + @"\uninstall.exe" + "\"";

            //it doesn't exist
            startupkey.SetValue("LogOff Utility", runDir);
            startupkey.Close();

            RegistryKey uninstallSubKey = uninstallkey.CreateSubKey("Logoff_Utility");
            if (uninstallSubKey != null)
            {
                uninstallSubKey.SetValue("DisplayName", "HTC Logoff Utility");
                uninstallSubKey.SetValue("UninstallString", uninstallString);
            }

            
        }


        static void Main(string[] args)
        {
            string dir32 = @"C:\Program Files\HTC-Logout";
            string dir64 = @"C:\Program Files (x86)\HTC-Logout";

            //delete the old files
            if (Directory.Exists(dir64))
            {
                deleteFiles(dir64);
                copyNewFiles(dir64);
                makeRegEntries(dir64);
            }
            else if (Directory.Exists(dir32))
            {
                deleteFiles(dir32);
                copyNewFiles(dir32);
                makeRegEntries(dir32);
            }
            else if (Directory.Exists(@"C:\Program Files (x86)"))
            {
                Directory.CreateDirectory(dir64);
                copyNewFiles(dir64);
                makeRegEntries(dir64);
            }
            else
            {
                Directory.CreateDirectory(dir32);
                copyNewFiles(dir32);
                makeRegEntries(dir32);
            }

            //debug to know it's done
            //Console.ReadLine();
            DateTime now = DateTime.Now;
            string timestring = now.ToShortTimeString();
            Console.WriteLine("Finished at " + timestring);

        }
    }
}
