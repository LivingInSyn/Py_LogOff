using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace HTC_LogOut
{
    public class LogOuter
    {

        [DllImport("user32.dll")]
        public static extern int ExitWindowsEx(int operationFlag, int operationReason);
        public void LogOffUser()
        {
            ExitWindowsEx(4, 0);
        }

        public void LockMachine()
        {
            System.Diagnostics.Process.Start(@"C:\WINDOWS\system32\rundll32.exe", "user32.dll,LockWorkStation");
        }
    }
}
