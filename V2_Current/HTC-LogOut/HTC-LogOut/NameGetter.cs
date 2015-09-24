using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.DirectoryServices.AccountManagement;

namespace HTC_LogOut
{
    public class NameGetter
    {
        public string get_displayName()
        {
            PrincipalContext ctx = new PrincipalContext(ContextType.Domain);
            UserPrincipal user = UserPrincipal.Current;
            string displayName = user.DisplayName;
            //return displayName;

            string name = user.GivenName + " " + user.Surname;
            if(name == " ")
            {
                name = Environment.UserName;
            }
            
            return name;
        }

        public string get_userName()
        {
            return Environment.UserName;
        }
    }
}
