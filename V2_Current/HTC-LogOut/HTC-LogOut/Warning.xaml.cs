using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace HTC_LogOut
{
    /// <summary>
    /// Interaction logic for Warning.xaml
    /// </summary>
    public partial class Warning : Page
    {

        public delegate void SendTime(string minutes, string hours);
        public static event SendTime onOkClick;

        public delegate void LogoutNow();
        public static event LogoutNow onLogOutNow;

        public Warning()
        {
            InitializeComponent();

            //make namegetter
            NameGetter namer = new NameGetter();
            string name = namer.get_displayName();

            TextLine1.Text = name + " is the currently logged in user.";
        }

        public void five_more(object sender, RoutedEventArgs e)
        {
            onOkClick("5", "0");
        }

        public void logout_now(object sender, RoutedEventArgs e)
        {
            onLogOutNow();
        }
    }
}
