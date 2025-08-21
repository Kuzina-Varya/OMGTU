using System.Collections;
using System.Globalization;

namespace очередь__словарь_хэштаблицы
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Queue number = new Queue();
            Queue date = new Queue();
            Queue timestart = new Queue();
            Queue time = new Queue();
            Console.WriteLine("Введите данные:");
            string str = Console.ReadLine();
            while (str != null)
            {
                number.Enqueue(str);
                str = Console.ReadLine();
                date.Enqueue(str);
                str = Console.ReadLine();
                timestart.Enqueue(str);
                str = Console.ReadLine();
                time.Enqueue(str);
                str = Console.ReadLine();
            }
            Console.WriteLine("Выберите какую задачу хотите выюрать:");
            Console.WriteLine("1-Месячный отчёт по общей сумме разговоров (минут) каждого номера ");
            Console.WriteLine("2-Суммарное время разговоров по каждому дню по всем номерам ");
            string operatoin = Console.ReadLine();
            int count = 0;
            switch (operatoin)
            {
                case "1":
                    Hashtable hashtable = new Hashtable();
                    for (int i = 0; i < number.Count; i++)
                    {
                        string num = Convert.ToString(number.Peek());
                        double min = Convert.ToDouble(time.Peek());

                        if (hashtable.ContainsKey(num))
                        {
                            hashtable[num] = min + Convert.ToDouble(hashtable[num]);
                        }
                        else hashtable.Add(num, min);

                    }
                    foreach (string key in hashtable.Keys) Console.WriteLine($"ХТ-Ключ_номер:{key},значение:{hashtable[key]}");
                    Dictionary<string, double> dictionary = new Dictionary<string, double>();
                    for (int i = 0; i < number.Count; i++)
                    {
                        string num = Convert.ToString(number.Peek());
                        double min = Convert.ToDouble(time.Peek());

                        if (dictionary.ContainsKey(num))
                        {
                            dictionary[num] += min;
                        }
                        else dictionary.Add(num, min);

                    }
                    foreach (string key in dictionary.Keys) Console.WriteLine($"Словарь-Ключ_номер:{key},значение:{dictionary[key]}");


                    break;
                case "2":
                    Hashtable hashtable2 = new Hashtable();
                    for (int i = 0; i < date.Count; i++)
                    {
                        string dat = Convert.ToString(date.Peek());
                        double min = Convert.ToDouble(time.Peek());

                        if (hashtable2.ContainsKey(dat))
                        {
                            hashtable2[dat] = min + Convert.ToDouble(hashtable2[dat]);
                        }
                        else hashtable2.Add(dat, min);


                    }
                    foreach (string key in hashtable2.Keys) Console.WriteLine($"ХТ-Ключ_дата:{key},значение:{hashtable2[key]}");
                    Dictionary<string, double> dictionary2 = new Dictionary<string, double>();
                    for (int i = 0; i < date.Count; i++)
                    {
                        string dat = Convert.ToString(date.Peek());
                        double min = Convert.ToDouble(time.Peek());

                        if (dictionary2.ContainsKey(dat))
                        {
                            dictionary2[dat] += min;
                        }
                        else dictionary2.Add(dat, min);


                    }
                    foreach (string key in dictionary2.Keys) Console.WriteLine($"Словарь-Ключ:{key},значение:{dictionary2[key]}");
                    break;
            }


        }
    }
}
