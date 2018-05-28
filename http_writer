using Codeplex.Data;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Grabber
{
    public partial class Form1 : Form
    {
       
        public Form1()
        {
            InitializeComponent();

            Fiddler.FiddlerApplication.AfterSessionComplete += FiddlerApplication_AfterSessionComplete;
            //Fiddler.CONFIG.IgnoreServerCertErrors = false;

            
        }

        delegate void SetTextCallback(string text);

        //定義

        public static class GlobalVar
        {
            public static int totalrank = 0;
            public static int member = 0;
            public static string guildname;
            public static string lupi;
            public static string url;
            //checkerが21と30の間のときに3ページ目にいったときに平均値を出すようにする
            public static int checker = 0;
            public static bool page1 = false;
            public static bool page2 = false;
            public static bool page3 = false;
            //団のプロフを通ってからじゃないと平均出したときに団名がでないときがある
            public static bool mainpage = false;
            //団のID用
            public static string guildidcheck= "initial";
            //１７５以上
            public static int over175 = 0;

        }

        //非公開の団用
        public static class hikoukaidan
        {
            public static string num_member = "";
            public static string average_rank = "";
            public static string active = "";
            public static bool check = false;
            //JSONファイルが平均ランクなどの情報→きくう団情報の順番なのでそのためのやつ
            public static bool check2 = false;
            public static bool check3 = false;
            //前の団とかぶらないように
            public static string url_saver = "1";
            public static bool daburi = false;
        }

        public class List
        {
            public string id { get; set; }
            public string level { get; set; }
            public bool is_leader { get; set; }
            public string member_position { get; set; }
            public string member_position_name { get; set; }
            public string name { get; set; }
            public string viewer_id { get; set; }
            public string image { get; set; }
            public string summon_id { get; set; }
            public string last_login { get; set; }
        }

        void guildname(Fiddler.Session oSession)
        {
            var a = oSession.GetResponseBodyAsString();
            Console.WriteLine(a);
            var test = DynamicJson.Parse(a);
            GlobalVar.guildname = "," + test.guild_name;
            GlobalVar.lupi = test.most_donated_lupi;
            GlobalVar.url = "http://game.granbluefantasy.jp/#guild/detail/" + test.guild_id;
            GlobalVar.guildidcheck = test.guild_id;

            writeGuildname(test.guild_name);
            GlobalVar.mainpage = true;

            //初期化
            GlobalVar.totalrank = 0;
            GlobalVar.member = 0;
            GlobalVar.page1 = false;
            GlobalVar.page2 = false;
            GlobalVar.page3 = false;
            GlobalVar.checker = 0;

            if (hikoukaidan.check == false)
            {
                writeGuildnum("");
                writeARank("");
            }

        }

        //非公開だん専用
        void hikoukai(Fiddler.Session oSession)
        {
            var a = oSession.GetResponseBodyAsString();

            
                hikoukaidan.check = true;
                string pattern1 = @"(prt-status-value%22%3E)(?<members>.+?)(%E4%BA%BA%3C%2Fdiv)";
                string pattern2 = @"(Rank%3C%2Fdiv%3E%0A%09%09%09%09%3Cdiv%20class%3D%22prt-status-value%22%3E)(?<members>.+?)(%3C%2Fdiv%3E%0A%09%09%09%3C%2Fdiv)";
                hikoukaidan.num_member = Regex.Match(a, pattern1).Groups["members"].Value;
                hikoukaidan.average_rank = Regex.Match(a, pattern2).Groups["members"].Value;
                Console.WriteLine(hikoukaidan.num_member + hikoukaidan.average_rank);

                writeGuildnum(hikoukaidan.num_member);
                writeARank(hikoukaidan.average_rank);
                hikoukaidan.check2 = false;

            
        }


            //write log in textbox
            void writeLog(String logText)
        {
            textBox1.SelectionStart = textBox1.Text.Length;
            textBox1.SelectionLength = 0;
            textBox1.SelectedText = logText + "\r\n";
            //textBox1.SelectedText = "[" + System.DateTime.Now.ToString() + "]" + logText + "\r\n";
        }


        void writeGuildname(String logText)
        {
            // InvokeRequired required compares the thread ID of the
            // calling thread to the thread ID of the creating thread.
            // If these threads are different, it returns true.
            if (this.textBox2.InvokeRequired)
            {
                SetTextCallback d = new SetTextCallback(writeGuildname);
                this.Invoke(d, new object[] { logText });
            }
            else
            {
                this.textBox2.Text = logText;
            }

            //textBox2.SelectionStart = textBox2.Text.Length;
            //textBox2.SelectionLength = 0;
            //textBox2.SelectedText = logText;
            //textBox1.SelectedText = "[" + System.DateTime.Now.ToString() + "]" + logText + "\r\n";
        }

        //textbox3に団員数をかく
        void writeGuildnum(String logText)
        {
            if (this.textBox3.InvokeRequired)
            {
                SetTextCallback d = new SetTextCallback(writeGuildnum);
                this.Invoke(d, new object[] { logText});
            }
            else
            {
                this.textBox3.Text =  logText;
            }

            //textBox3.SelectionStart = textBox3.Text.Length;
            //textBox3.SelectionLength = 0;
            //textBox3.SelectedText = "/" + logText;
            //textBox1.SelectedText = "[" + System.DateTime.Now.ToString() + "]" + logText + "\r\n";
        }

        //textbox4に平均ランク
        void writeARank(String logText)
        {
            if (this.textBox4.InvokeRequired)
            {
                SetTextCallback d = new SetTextCallback(writeARank);
                this.Invoke(d, new object[] { logText });
            }
            else
            {
                this.textBox4.Text = logText;
            }

      
        }

        //本体---------------------------------------------------------------------------------------------------------------------
        void FiddlerApplication_AfterSessionComplete(Fiddler.Session oSession)
        {
            var path = oSession.PathAndQuery;

            if (!path.StartsWith("/guild_other/member_list/")) // 団員一覧のAPI以外は無視する
            {
                if (path.StartsWith("//guild_other/guild_info"))
                {
                    guildname(oSession);
                    if (hikoukaidan.check2 == false)
                    {
                        Console.WriteLine("unchi");
                        show();
                    }
                }

                /*団プロフ通ってない時はスルー？
                if(path.Contains(GlobalVar.guildidcheck) == false)
                {
                    oSession.Ignore();
                    return;
                }
                */

                //非公開の団を探す
                if (path.StartsWith("/guild_main/content/detail/"))
                {
                    hikoukai(oSession);
                    
                }

                    oSession.Ignore();
                return;
            }
            //コンソールに書く
            Console.WriteLine(oSession.fullUrl);
            //セッション情報をjson化して解析
            var a = oSession.GetResponseBodyAsString();
            Console.WriteLine(a);
            var test = DynamicJson.Parse(a);
            int index = 0;

            //団プロフ→1ページ目に飛ぶことを想定
            if (test.current == "1" && GlobalVar.page1 == false && path.Contains(GlobalVar.guildidcheck) == true)
            {
                foreach (int x in test.list)
                {
                    if (int.Parse(test.list[index].level) >= 175) GlobalVar.over175++;
                    GlobalVar.totalrank += int.Parse(test.list[index].level);
                    //var r1 = test.list[index].level;
                    //Console.WriteLine(r1);
                    index++;
                    GlobalVar.checker++;
                    GlobalVar.page1 = true;

                    
                }
                //intをstringにキャスト
                string s = GlobalVar.checker.ToString();
                writeGuildnum(s + "/" + test.count);
            }

            //2ページ目初回のみカウント
            if (test.current == "2" && GlobalVar.page2 == false && path.Contains(GlobalVar.guildidcheck) == true)
            {
                foreach (int x in test.list)
                {
                    if (int.Parse(test.list[index].level) >= 175) GlobalVar.over175++;
                    GlobalVar.totalrank += int.Parse(test.list[index].level);
                    index++;
                    GlobalVar.checker++;
                    GlobalVar.page2 = true;


                }
                //intをstringにキャスト
                string s = GlobalVar.checker.ToString();
                writeGuildnum(s + "/" + test.count);
            }

            //3ページ目初回時のみカウント
            if (test.current == "3" && GlobalVar.page3 == false && path.Contains(GlobalVar.guildidcheck) == true)
            {
                foreach (int x in test.list)
                {
                    if (int.Parse(test.list[index].level) >= 175) GlobalVar.over175++;
                    GlobalVar.totalrank += int.Parse(test.list[index].level);
                    index++;
                    GlobalVar.checker++;
                    GlobalVar.page3 = true;
                }
                //intをstringにキャスト
                string s = GlobalVar.checker.ToString();
                writeGuildnum(s + "/" + test.count);
            }

            //GlobalVar.member += index;
            GlobalVar.member = (int)test.count;



            //どのページでも団員数さえ満たしているならおっけ
            //test.countは団員数
            if (GlobalVar.checker == test.count && GlobalVar.mainpage == true && path.Contains(GlobalVar.guildidcheck) == true)
            {
                Console.WriteLine("kuso");
                show();
            }

            


            //var arrayJson = DynamicJson.Parse(a);
            //var json = arrayJson.Deserialize<List>();
            //var r1 = json.id;
            // Console.WriteLine(r1);
        }

        


        //write log
        void show()
        {
            if (InvokeRequired)
            {
                MethodInvoker method = new MethodInvoker(show);
                Invoke(method);
                return;
            }

            

                string averagerank;
                //int→string
                string converter;
                //非公開の団と合わせるために小数点以下をきったデータも表示
                string converter2;
                //なんだろう
                double average1;
                average1 = ((double)GlobalVar.totalrank / (double)GlobalVar.member);
                //double->string
                converter = average1.ToString("f2");
                converter2 = average1.ToString("f0");
                averagerank = "," + converter;
                writeLog(GlobalVar.guildname + "," + hikoukaidan.num_member + "," + hikoukaidan.average_rank +"," + GlobalVar.lupi + ",<a href=" + "\""+ GlobalVar.url  + "\""+ " target=" + "\"" + "blank" + "\"" + ">" + GlobalVar.guildidcheck + "</a>,");
                writeARank(converter);


             

            GlobalVar.totalrank = 0;
            GlobalVar.member = 0;
            GlobalVar.guildname = "";
            GlobalVar.page1 = false;
            GlobalVar.page2 = false;
            GlobalVar.page3 = false;
            GlobalVar.checker = 0;
            GlobalVar.mainpage = false;
            GlobalVar.lupi = "";
            GlobalVar.over175 = 0;
            hikoukaidan.average_rank = "";
            hikoukaidan.num_member = "";
            hikoukaidan.check = false;
            hikoukaidan.check2 = false;
        }

       

        //団員数が20人以下のときはボタンで計算
        private void button3_Click(object sender, EventArgs e)
        {
            show();
        }

        //CTRL+Aで全部コピー
        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Control && e.KeyCode == Keys.A)
                textBox1.SelectAll();
                textBox1.Copy();
        }


        /// <summary>
        /// キャプチャ開始
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void button1_Click(object sender, EventArgs e)
        {
            //すべての通信をキャプチャ
            Fiddler.FiddlerApplication.Startup(0,Fiddler.FiddlerCoreStartupFlags.DecryptSSL | ~Fiddler.FiddlerCoreStartupFlags.ChainToUpstreamGateway);
            Fiddler.URLMonInterop.SetProxyInProcess(string.Format("{0}:{1}", "127.0.0.1:{0}",Fiddler.FiddlerApplication.oProxy.ListenPort), "<local>");
            
        }

        /// <summary>
        /// キャプチャ終了
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void button2_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Debug.WriteLine("Shutting down...");
            Fiddler.FiddlerApplication.Shutdown();
            this.Close();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }

}
