using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
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
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : NavigationWindow
    {

        private int mins;
        private int hrs;

        private int times_warn_called;

        private static int warning_time;
        private static int hourNoInputTime;

        private static Timer five_min_timer;
        private static Timer no_input_timer;

        private static LogOuter logouter;

        private static Logger logs;

        //private Five_Min_Timer timer;

        public MainWindow()
        {
            InitializeComponent();

            //init times_warn_called to 0
            times_warn_called = 0;

            //set warning_time to 300000, 5 minutes in ms
            warning_time = 300000;
            //set the hourNoInputTime to 1 hour in ms
            hourNoInputTime = 3600000;


            //make an instance of logouter
            logouter = new LogOuter();

            //make an instance of the timer
            //timer = new Five_Min_Timer();

            //make the new version of the timer
            five_min_timer = new Timer(1000);
            five_min_timer.Elapsed += new ElapsedEventHandler(OnTimedEvent);
            five_min_timer.Enabled = false;

            //make the no input timer, this one starts automatically
            no_input_timer = new Timer(1000);
            no_input_timer.Elapsed += new ElapsedEventHandler(OnNoInputEvent);
            no_input_timer.Enabled = true;

            //these are all of the event listeners for on_OkClick which handles setting up the initial sleep time
            CustomTimePage.onOkClick += CustomTimePage_onOkClick;
            BadTimePage.onOkClick += CustomTimePage_onOkClick;
            Warning.onOkClick += CustomTimePage_onOkClick;
            SelectHoursPage.onOkClick += CustomTimePage_onOkClick;

            //this event listener is for when the 5 minutes are up!
            //Five_Min_Timer.timer_up += timer_up;

            //the event handler for when Logout Now is clicked
            Warning.onLogOutNow += Warning_LogOutNow;

            //event handler for detecting a manually initiated logout
            SystemEvents.SessionEnding += Detect_Logout;

            //create the logger
            logs = new Logger();
            logs.start_log();
            
        }


        protected override void OnClosing(CancelEventArgs e)
        {
            //base.OnClosing(e);
            e.Cancel = true;
            base.OnClosing(e);
        }

        private static void OnTimedEvent(object source, ElapsedEventArgs e)
        {
            Debug.WriteLine("ping");
            decrease_warning();
        }

        private static void OnNoInputEvent(object source, ElapsedEventArgs e)
        {
            Debug.WriteLine("ping");
            decrease_hourTimer();
        }

        private static void decrease_warning()
        {
            warning_time = warning_time - 1000;
            Debug.WriteLine(warning_time);
            if (warning_time <= 0)
            {
                timer_up();
            }
        }

        private static void decrease_hourTimer()
        {
            hourNoInputTime = hourNoInputTime - 1000;
            Debug.WriteLine(hourNoInputTime);
            if (hourNoInputTime <= 0)
            {
                timer_up();
            }
        }

        private static void timer_up()
        {
            Debug.WriteLine("THE TIMER IS UP");
            logs.logAutoLogOff();
            logouter.LogOffUser();
        }

        void Warning_LogOutNow()
        {
            Debug.WriteLine("LOGOUT NOW CLICKED");
            logs.logLogoutNow();
            logouter.LogOffUser();
        }

        void CustomTimePage_onOkClick (string minutes, string hours)
        {
            Debug.WriteLine(minutes);
            Debug.WriteLine(hours);

            //STOP THE NO INPUT TIMER DUMMY
            no_input_timer.Enabled = false;

            //check to see if it's been called more than 3 times
            if (times_warn_called > 3)
            {
                logs.logAutoLogOff();
                logouter.LogOffUser();
            }

            bool goodmin = false;
            bool goodhr = false;

            five_min_timer.Enabled = false;
            warning_time = 300000;
            
            if(minutes == "")
            {
                minutes = "0";
            }
            if(hours == "")
            {
                hours = "0";
            }

            //try to parse minutes
            if (Int32.TryParse(minutes,out mins))
            {
                if(mins >= 0 && mins < 60)
                {
                    goodmin = true;
                }
            }
            

            //try to parse hrs
            if (Int32.TryParse(hours, out hrs))
            {
                if(hrs >= 0 && hrs < 8)
                {
                    goodhr = true;
                }                
            }

            if(hrs == 0 && mins == 0)
            {
                //setting just one to false is good enough
                goodhr = false;
            }

            //if both are good:
            if (goodhr && goodmin)
            {
                int total_mins = (hrs * 60) + mins;
                logs.logSelection(minutes, hours);
                this.Hide();

                //make warning instance
                Warning warning = new Warning();
                //navigate to it
                this.Navigate(warning);

                System.Threading.Thread.Sleep(total_mins * 60 * 1000);
                this.Show();

                //start the timer
                five_min_timer.Enabled = true;

                //increase times_warning_called
                times_warn_called = times_warn_called + 1;
                            
            }
            else
            {
                BadTimePage badtime = new BadTimePage();
                this.Navigate(badtime);
            }
        }

        private void Detect_Logout(object sender, EventArgs e)
        {
            Application.Current.Shutdown();            
        }


    }
}
