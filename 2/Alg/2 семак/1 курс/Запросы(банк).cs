using System;
using System.Collections.Generic;
using System.Linq;
namespace запросы_банк_
{
    class Person
    {
        public int Account_number { get; set; }
        public string Full_name { get; set; }
        public int Income { get; set; }
        public int Consumption { get; set; }
        public int Tax { get; set; }
        public static void Print(IEnumerable<Person> numQuery1)
        {
            foreach (Person person in numQuery1)
            {
                Console.WriteLine($"Номер счета: {person.Account_number}");
                Console.WriteLine($"ФИО: {person.Full_name}");
                Console.WriteLine($"Доход: {person.Income}");
                Console.WriteLine($"Расход: {person.Consumption}");
                Console.WriteLine($"Налог: {person.Tax}");
                Console.WriteLine();
            }
                
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            string[] names = {"Пупкин Иван Васильевич","Сухая Кажура Ивановна","Михайлов Михаил Михайлович","Многоэтажева Екатерина Антоновна","Застольнай Игорь Иванович" };
            int[] ints = {25000,14000,1250,52000,23000,1150,-92,586,5,-9654,4521,483,6789,155,340 };
            List<Person> list = new List<Person>();
            Random random = new Random();
            Person person= new Person();
            for (int i = 0,j = 0;i<ints.Length&&j<names.Length; i+=3,j++)
            {
                


                person.Account_number = random.Next(1, 154);
                
                 person.Full_name = names[j];
                    person.Income = ints[i];
                    person.Consumption = ints[i + 1];
                    person.Tax = ints[i + 2];

                
                
                
                   
                
                
                list.Add(person);
                person = new Person();

                
            }
            Console.WriteLine("1-Количество клиентов с отрицательным балансом:");
            IEnumerable<Person> numQuery1 = from p in list where (p.Income-p.Consumption < 0) select p;
            Person.Print(numQuery1);
            Console.WriteLine(numQuery1.Count());
            Console.WriteLine("-----------------------------");
            Console.WriteLine("2-Клиент с самым большим балансом с учетом оплаты налогов:");
            Console.WriteLine(list.Max(p => (p.Income - p.Consumption - p.Tax)));
            Console.WriteLine("3-Средний доход по считам с отрицательным балансам:");
            Console.WriteLine(numQuery1.Average(p=>p.Income));
            Console.WriteLine("4-Суммарный налог со всех клиентов:");
            Console.WriteLine(list.Sum(p => p.Tax));
        }
    }
}
