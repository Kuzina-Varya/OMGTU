using System.Collections.Generic;
using System.Numerics;
namespace обощения
{

    internal class Program
    {
        static void Menu1()
        {
            Console.WriteLine("Выберите с какими числами хотите работать:");
            Console.WriteLine("1-с целыми");
            Console.WriteLine("2-с вещественными");
        }
        static void Menu2()
        {
            Console.WriteLine("Выберете операцию с цислами,которую хотите совершить:");
            Console.WriteLine("1-Сложение");
            Console.WriteLine("2-Вычитание");
            Console.WriteLine("3-Умножение");
            Console.WriteLine("4-Деление");
        }
        static void Sum<T>(ref T x, ref T y) 
        {
            dynamic s = x;
            s += y;
            Console.WriteLine(s); 


        }
        static void Subtraction<T>(ref T x, ref T y) 
        {
            dynamic s = x;
            s -= y;
            Console.WriteLine(s);
        }
        static void Multiplication<T>(ref T x, ref T y) 
        {
            dynamic s = x;
            s *= y;
            Console.WriteLine(s);
        }
        static void Division<T>(ref T x, ref T y) 
        {
            dynamic s = x;
            s /= y;
            Console.WriteLine(s);
        }

        static void Main(string[] args)
        {
            Menu1();
            string operation1 = Console.ReadLine();
            Menu2();
            string operation2 = Console.ReadLine();
            while (operation1 != null)
            {
                switch (operation1)
                {
                    case "1":
                        while (operation2 != null)
                        {
                            switch (operation2)
                            {
                                case "1":
                                    Console.WriteLine("Введите 2 числа,которые хотите сложить:");
                                    int x1 = Convert.ToInt32(Console.ReadLine());
                                    int x2=Convert.ToInt32(Console.ReadLine());
                                    Sum(ref x1, ref x2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "2":
                                    Console.WriteLine("Введите 2 числа,которые хотите вычесть:");
                                    x1 = Convert.ToInt32(Console.ReadLine());
                                    x2 = Convert.ToInt32(Console.ReadLine());
                                    Subtraction(ref x1, ref x2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "3":
                                    Console.WriteLine("Введите 2 числа,которые хотите умножить:");
                                    x1 = Convert.ToInt32(Console.ReadLine());
                                    x2 = Convert.ToInt32(Console.ReadLine());
                                    Multiplication(ref x1, ref x2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "4":
                                    Console.WriteLine("Введите 2 числа,которые хотите разделить:");
                                    x1 = Convert.ToInt32(Console.ReadLine());
                                    x2 = Convert.ToInt32(Console.ReadLine());
                                    Division(ref x1, ref x2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                            }
                            Menu1();
                            operation1 = Console.ReadLine();
                            Menu2();
                            operation2 = Console.ReadLine();
                        }
                        break;
                    case "2":
                        while (operation2 != null)
                        {
                            switch (operation2)
                            {
                                case "1":
                                    Console.WriteLine("Введите 2 числа,которые хотите сложить:");
                                    double y1=Convert.ToDouble(Console.ReadLine());
                                    double y2=Convert.ToDouble(Console.ReadLine());
                                    Sum(ref y1, ref y2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "2":
                                    Console.WriteLine("Введите 2 числа,которые хотите вычесть:");
                                    y1 = Convert.ToDouble(Console.ReadLine());
                                    y2 = Convert.ToDouble(Console.ReadLine());
                                    Subtraction(ref y1, ref y2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "3":
                                    Console.WriteLine("Введите 2 числа,которые хотите умножить:");
                                    y1 = Convert.ToDouble(Console.ReadLine());
                                    y2 = Convert.ToDouble(Console.ReadLine());
                                    Multiplication(ref y1, ref y2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                                case "4":
                                    Console.WriteLine("Введите 2 числа,которые хотите разделить:");
                                    y1 = Convert.ToDouble(Console.ReadLine());
                                    y2 = Convert.ToDouble(Console.ReadLine());
                                    Division(ref y1, ref y2);
                                    Menu2();
                                    operation2 = Console.ReadLine();
                                    break;
                            }
                            Menu1();
                            operation1 = Console.ReadLine();
                            Menu2();
                            operation2 = Console.ReadLine();
                        }
                        break;
                }
            }

        }
    }
}
