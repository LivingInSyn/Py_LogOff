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
    /// Interaction logic for BadTimePage.xaml
    /// </summary>
    public partial class BadTimePage : Page
    {
        public delegate void SendTime(string minutes, string hours);
        public static event SendTime onOkClick;

        public BadTimePage()
        {
            InitializeComponent();
        }

        private void go_back(object sender, RoutedEventArgs e)
        {
            SelectHoursPage hourspage = new SelectHoursPage();
            this.NavigationService.Navigate(hourspage);
        }

        private void ok_click(object sender, RoutedEventArgs e)
        {
            string minutes = badminuteBox.Text;
            string hours = badhourBox.Text;
                        
            onOkClick(minutes, hours);

        }
    }
}
