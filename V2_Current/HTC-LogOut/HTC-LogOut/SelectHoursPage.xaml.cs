using System;
using System.Collections.Generic;
using System.Diagnostics;
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
    /// Interaction logic for SelectHoursPage.xaml
    /// </summary>
    public partial class SelectHoursPage : Page
    {

        public delegate void SendTime(string minutes, string hours);
        public static event SendTime onOkClick;

        public SelectHoursPage()
        {
            InitializeComponent();
        }

        private void custom_time(object sender, RoutedEventArgs e)
        {
            CustomTimePage custom_time = new CustomTimePage();
            this.NavigationService.Navigate(custom_time);
        }

        private void preset_time(object sender, RoutedEventArgs e)
        {
            Button _button = (Button)sender;
            //arg is the tag, which is the number of hours
            string arg = _button.Tag.ToString();
            Debug.WriteLine(arg);

            if (arg == "1.5")
            {
                onOkClick("30", "1");
            }
            else
            {
                onOkClick("0", arg);
            }

            
        }
    }
}
