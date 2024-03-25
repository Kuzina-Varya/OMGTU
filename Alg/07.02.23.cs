using System.ComponentModel;
using System.Threading.Channels;

namespace _07_02_23
{
    class Menu
    {
        public string first = "1.  Создание базы данных";
        public string second = "2.  Добавление в базу данных новой информации";
        public string fird = "3.  Изменение данных аудитории по заданному номеру";
        public string fourth = "4.  Выбор аудиторий с количествомвом посадочных мест больше или равным заданного";
        public string fiveth = "5.  Выбор аудиторий с проектором ";
        public string sixth = "6.  Выбор аудиторий с пк и заданным количеством посадочных мест";
        public string seventh = "7.  Выбор аудиторий по номеру этажа";
        public string eiugth = "8.  Вывод всех данных по аудиториям";
        public string nineth = "9.  Выход";

        public void StartMenu()
        {
            Console.WriteLine("Меню:");
            Console.WriteLine(first);
            Console.WriteLine(second);
            Console.WriteLine(fird);
            Console.WriteLine(fourth);
            Console.WriteLine(fiveth);
            Console.WriteLine(sixth);
            Console.WriteLine(seventh);
            Console.WriteLine(eiugth);
            Console.WriteLine(nineth);
        }
        public void EndMenu()
        {

            Console.WriteLine("1-Номер аудитории");
            Console.WriteLine("2-Количество мест");
            Console.WriteLine("3-Наличие проектора");
            Console.WriteLine("4-Наличие пк");
        }

    }
    class Base
    {
       
        public int Classroom { get; set; }
        public int Pk { get; set; }
        public int Proektor { get; set; }
        public int Sit { get; set; }
        public Base()
        {
           
        }
        public void index7(int etaj, List<Base> list)
        {
            for(int i = 0; i < list.Count; i++)
            {
                if (list[i].Classroom %10 == etaj)
                {
                    Console.WriteLine(list[i].Classroom);
                }
            }
        }

        public void index6(int cheers, List<Base> list)
        {
            for (int i = 0; i < list.Count; i++)
            {
                if ((list[i].Pk == 1) && (list[i].Sit >= cheers))
                {
                    Console.WriteLine(list[i].Classroom);
                }
            }
        }
        public void index4(int value, List<Base> list)
        {
            for (int i = 0; i < list.Count; i++)
            {
                i++;
                if (list[i].Classroom >= value)
                {
                    Console.WriteLine(list[i].Classroom);
                }
                
            }
        }
        public void index5(List<Base> list)
        {
            for (int i = 0; i < list.Count; i++)
            {
                if (list[i].Pk == 1)
                {
                    Console.WriteLine(list[i].Classroom);
                }
            }
        }
        public void find(int operation, int replecement, int replecement2, List<Base> list)
        {

            for (int i = 0; i < list.Count; i++)
            {

                if (operation == 1)
                {
                    if (list[i].Classroom == replecement)
                    {
                        list[i].Classroom = replecement2;

                        break;
                    }
                }
                if (operation == 2)
                {
                    if (list[i].Sit == replecement)
                    {
                        list[i].Sit = replecement2;

                        break;
                    }
                }
                if (operation == 3)
                {
                    if (list[i].Proektor == replecement)
                    {
                        list[i].Proektor = replecement2;

                        break;
                    }
                }
                if (operation == 4)
                {
                    if (list[i].Pk == replecement)
                    {
                        list[i].Pk = replecement2;

                        break;
                    }
                }
            }

        }
        public void proverka(int operat, int e2, List<Base> list, Base univercity)
        {
            if (operat == 1)
            {

                while ((e2 / 100 > 10) || (e2 / 100 == 0) || (e2 % 10 > 10) || (e2 % 10 == 0))
                {
                    Console.WriteLine("Ведите другое число! Первые 2 цифры которого обозначают номер аудитории, а последняя номер этажа");
                    e2 = Convert.ToInt32(Console.ReadLine());

                }
                univercity.Classroom = e2;
                


            }
            if (operat == 2)
            {

                while (e2 == 0)
                {
                    Console.WriteLine("Введите другое число");
                    e2 = Convert.ToInt32(Console.ReadLine());
                }
                univercity.Sit = e2;
                
            }
            if (operat == 3)
            {

                while ((e2 != 0) && (e2 != 1))
                {
                    Console.WriteLine("Введите число, раное 0 или 1, где 0-если нет проектора в аудитории,а 1-есть ");
                    e2 = Convert.ToInt32(Console.ReadLine());
                }
                univercity.Proektor = e2;
               
            }
            if (operat == 4)
            {

                while ((e2 != 0) && (e2 != 1))
                {
                    Console.WriteLine("Введите число, раное 0 или 1, где 0-если нет пк в аудитории,а 1-есть ");
                    e2 = Convert.ToInt32(Console.ReadLine());
                }
                univercity.Pk = e2;
                
            }


        }
        public void print(List<Base> list)
        {
            for (int i = 0; i < list.Count; i++)
            {
                Console.Write(list[i].Classroom+" ");
                Console.Write(list[i].Pk+" ");
                Console.Write(list[i].Proektor+" ");
                Console.Write(list[i].Sit + " ");
                Console.WriteLine();
            }
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            Menu startmenu = new Menu();
            startmenu.StartMenu();
            Console.WriteLine("Введите выбранную операцию:");
            int operation = Convert.ToInt32(Console.ReadLine());
            Base univer = new Base();
            Base univercity = new Base();
            List<Base> list = new List<Base>();
            while (operation != 9)
            {

                while ((operation > 9) || (operation == 0))
                {

                    Console.WriteLine("Введите число от 1 до 9");
                    operation = Convert.ToInt32(Console.ReadLine());
                }
                switch (operation)
                {
                    case 1:
                        Console.WriteLine("Введите номер кабинета:");
                        int e1 = Convert.ToInt32(Console.ReadLine());
                        univercity.proverka(1, e1, list, univercity);

                        Console.WriteLine("Количество мест в аудитории:");
                        int b1 = Convert.ToInt32(Console.ReadLine());

                        univercity.proverka(2, b1, list, univercity);

                        Console.WriteLine("Введите 0-если нет проектора в аудитории, 1- если есть:");
                        int c1 = Convert.ToInt32(Console.ReadLine());

                        univercity.proverka(3, c1, list, univercity);

                        Console.WriteLine("Наличие пк в аудитории(если есть пк,то вводится 1,если нет-0):");
                        int d1 = Convert.ToInt32(Console.ReadLine());

                        univercity.proverka(4, d1,list, univercity);

                        list.Add(univercity);

                        Console.WriteLine("_________________________________________________________________________________");
                        Console.WriteLine("Проверьте введенную информацию:");
                        univercity.print(list);
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());

                        break;

                    case 2:
                        Console.WriteLine("Введите что вы хотите добавить в базу:");
                        startmenu.EndMenu();
                        int operat = Convert.ToInt32(Console.ReadLine());

                        Console.WriteLine("Введите значение:");
                        int value = Convert.ToInt32(Console.ReadLine());
                        univer.proverka(operat, value,list, univer);
                        list.Add(univer);
                        Console.WriteLine("_________________________________________________________________________________");
                        Console.WriteLine("Проверьте введенную информацию:");
                        univer.print(list);

                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 3:
                        Console.WriteLine("Введите что вы хотите изменить в базе данных:");
                        startmenu.EndMenu();
                        int option = Convert.ToInt32(Console.ReadLine());
                        Console.WriteLine("Какое значение вы хотите заменить:");
                        int replacement = Convert.ToInt32(Console.ReadLine());
                        Console.WriteLine("Введите новое значение:");
                        int replecment2 = Convert.ToInt32(Console.ReadLine());
                        univercity.find(option, replacement, replecment2, list);


                        univer.find(option, replacement, replecment2, list);
                        Console.WriteLine("_________________________________________________________________________________");
                        Console.WriteLine("Проверьте введенную информацию:");
                        univercity.print(list);
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());


                        break;
                    case 4:
                        Console.WriteLine("Введите количество посадочных мест:");
                        int pleces = Convert.ToInt32(Console.ReadLine());
                        Console.WriteLine("-----------------------------------------------------------------------------------");
                        univercity.index4(pleces, list);
                        univer.index4(pleces, list);
                        Console.WriteLine("-------------------------------------------------------------------------------------");
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 5:
                        Console.WriteLine("Аудитории с проектором:");
                        univercity.index5(list);
                        univer.index5(list);
                        Console.WriteLine("-------------------------------------------------------------------------------------");
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 6:
                        Console.WriteLine("Введите количество пасадочных мест:");
                        int cheers = Convert.ToInt32(Console.ReadLine());
                        univercity.index6(cheers, list);
                        univer.index6(cheers, list);
                        Console.WriteLine("-------------------------------------------------------------------------------------");
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());

                        break;
                    case 7:
                        Console.WriteLine("Введите номер этажа:");
                        int etaj = Convert.ToInt32(Console.ReadLine());
                        univercity.index7(etaj, list);
                        univer.index7(etaj, list);
                        Console.WriteLine("-------------------------------------------------------------------------------------");
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;
                    case 8:
                        univercity.print(list);
                        univer.print(list);
                        Console.WriteLine("-------------------------------------------------------------------------------------");
                        Console.WriteLine("Введите выбранную операцию:");
                        operation = Convert.ToInt32(Console.ReadLine());
                        break;



                }
            }
            Console.WriteLine("Выход из базы данных...");
            Console.ReadKey();
        }
    }
}
