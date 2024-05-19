using static System.Runtime.InteropServices.JavaScript.JSType;

namespace phone_base
{/*На вход подаётся данные типа: номер телефона с которого звонили, номер на который звонили, дата звонка, количество минут;
  * определить на какой номер чаще всего звонил выбранный абонент по датам(сгрупировав данные по датам),
  * определить номера с которыми наибольшее количество минут разговаривал абонент(каждый абонент)(сгрупировав данные по дате)
  */
    internal class Program
    {
        class Phone_base
        {
            private string phone_number_from;
            private string phone_number_where;
            private string dates;
            private string minutes;
            public string Phone_number_from {  get { return phone_number_from; } set { phone_number_from = value; } }
            public string Phone_number_where { get {  return phone_number_where; } set { phone_number_where = value; } }
            public string Date { get { return dates; } set { dates = value; } }
            public string Minutes {  get { return minutes; } set {  minutes = value; } }
            public Phone_base(string phone_from,string phone_where,string date,string minute) 
            {
                Phone_number_from = phone_from;
                Phone_number_where = phone_where;
                Date = date;
                Minutes = minute;
            }
        }

        static void Main(string[] args)
        {
            string end = "END";
            Console.WriteLine("Введите "+end+" когда закончите ввод в базу! ");
            Console.WriteLine("Введите номер с которго звонили:");
            string str=Console.ReadLine();
            List<Phone_base> list = new List<Phone_base>();
            string s = ":";
            while (str != end)
            {
                
                string phone_from = str;
                Console.WriteLine("Введите номер на который звонили:");
                string phone_where = Console.ReadLine();
                Console.WriteLine("Введите дату звонка:");
                string date = Console.ReadLine();
                Console.WriteLine("Введите количество минут:");
                str= Console.ReadLine();
                string minute="";
                if(str.Contains(s))
                {
                    minute = str.Replace(s, ",");
                }
                Phone_base phone_base1 = new Phone_base(phone_from, phone_where, date, minute);
                list.Add(phone_base1);
                Console.WriteLine("Введите номер с которго звонили:");
                str = Console.ReadLine();
                
            }
            Console.WriteLine("Введите номер абонента для которого вы хотите узнать кому он чаще всего звонил:");
            string find_number_call = Console.ReadLine();
            int number = 0; int count = 0; int max = 0;
            for (int i = 0; i < list.Count-1; i++)
            {
                for (int j = 1; j < list.Count ; j++)
                {
                    count = 0;
                    if ((list[i].Phone_number_from == find_number_call) && (list[i].Date == list[j].Date) && (list[i].Phone_number_where == list[j].Phone_number_where))
                    {
                        count++;
                        number = i;
                        if (count > max)
                        {
                            max = count;
                            Console.WriteLine($"дата:{list[number].Date}, кому звонил болльше всего:{list[number].Phone_number_where}");
                        }
                        
                    }
                   /* if((list[j].Phone_number_from == find_number_call) && (list[i].Date == list[j].Date) && (list[i].Phone_number_where == list[j].Phone_number_where))
                    {
                        count++;
                        number = i;
                        if (count > max)
                        {
                            max = count;
                            Console.WriteLine($"дата:{list[number].Date}, кому звонил болльше всего:{list[number].Phone_number_where}");
                        }
                    }*/

                }

            }
            Console.WriteLine("Определить номера с которыми наибольшее количество минут разговаривал каждый абонент:");
            
             number = 0; count = 0; max = 0;int index=0;
            for (int i = 0; i < list.Count - 1; i++)
            {
                for (int j = 1; j < list.Count; j++)
                {
                    count = 0;
                    if ((list[i].Phone_number_from == list[j].Phone_number_from) && (list[i].Date == list[j].Date))
                    {
                        count =Convert.ToInt32( Math.Max(Convert.ToDouble(list[i].Minutes), Convert.ToDouble(list[j].Minutes)));
                        index = (Convert.ToInt32(list[i].Minutes))==count?index=i:index=j;
                     
                        if (count > max)
                        {
                            max = count;
                            Console.WriteLine($"дата:{list[index].Date}, с кем разговаривал дольше всего:{list[index].Phone_number_where}");
                        }

                    }

                }

            }
            //List<Phone_base> copy = list.GetRange(0, list.Count());

            

            Console.WriteLine("---------------------------------------------------------------------------------------------");
            for (int i = 0; i < list.Count; i++) 
            {
                Console.Write(list[i].Phone_number_from+" ");
                Console.Write(list[i].Phone_number_where + " ");
                Console.Write(list[i].Date + " ");
                Console.Write(list[i].Minutes + " ");
                Console.WriteLine();
            }
        }
    }
}
