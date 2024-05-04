interface IMath
{
    public static double Sum(double x,double y)
    {
        return x + y;
    }
    public static double Subtraction(double x, double y)
    {
        return x - y;
    }
    public static double Multiplication(double x, double y)
    {
        return x * y;
    }
    public static double Division(double x, double y)
    {
        return Math.Round(x /y);
    }
    public static double Sqrt(double x)
    {
        return Math.Round(Math.Sqrt(x));
    }
    public static double Sin(double x)
    {
        return Math.Round(Math.Sin(x));
    }
    public static double Cos(double x)
    {
        return Math.Round(Math.Cos(x));//в радианах=>pi/3
    }

    static void Menu(string[] cars)
    {
        Console.WriteLine("Введите какое действие вы хотите совершить:");
        for (int i = 0; i < 7; i++)
        {
            Console.WriteLine($"{i + 1}_ {cars[i]}");
        }

    }

}

delegate double Parametr(double x);
delegate double Parametrs(double x,double y);

namespace интерфейсы_и_делегаты1
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string[] chars = { "+", "-", "*", "/", "корень", "sin", "cos" };
            IMath.Menu(chars);
            
            string str = Console.ReadLine();
            while (str != null)
            {
                switch (str)
                {
                    case "1":
                        Console.WriteLine("Введите два значения,которые нужно сложить:");
                        double x = Convert.ToDouble(Console.ReadLine());
                        double y = Convert.ToDouble(Console.ReadLine());
                        Parametrs pars=IMath.Sum;
                        Console.WriteLine(pars(x,y));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "2":
                        Console.WriteLine("Введите два значения,где первое-уменьшаемое, второе-вычитаемое:");
                        x = Convert.ToDouble(Console.ReadLine());
                        y = Convert.ToDouble(Console.ReadLine());
                        pars = IMath.Subtraction;
                        Console.WriteLine(pars(x, y));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "3":
                        Console.WriteLine("Введите два значения,где первое-множитель1, второе-множитель2:");
                        x = Convert.ToDouble(Console.ReadLine());
                        y = Convert.ToDouble(Console.ReadLine());
                        pars = IMath.Multiplication;
                        Console.WriteLine(pars(x, y));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "4":
                        Console.WriteLine("Введите два значения,где первое-делимое, второе-делитель:");
                        x = Convert.ToDouble(Console.ReadLine());
                        y = Convert.ToDouble(Console.ReadLine());
                        pars = IMath.Division;
                        
                        while (y == 0)
                        {
                            Console.WriteLine("Делитель не может быть равено 0!");
                            y = Convert.ToDouble(Console.ReadLine());
                        }
                        Console.WriteLine(pars(x, y));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "5":
                        Console.WriteLine("Введите значение,которое больше либо равно 0:");
                        x = Convert.ToDouble(Console.ReadLine());
                        
                        Parametr par = IMath.Sqrt;
                        while(x<0)
                        {
                            Console.WriteLine("Введите чило больше либо равное 0!");
                            x = Convert.ToDouble(Console.ReadLine());
                        }
                        Console.WriteLine(par(x));
                        
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "6":
                        Console.WriteLine("Введите значение в градусах:");
                        x =Math.PI* Convert.ToDouble(Console.ReadLine())/180.0;

                        par = IMath.Sin;
                       /* while (x < 0)
                        {
                            Console.WriteLine("Введите чило больше либо равное 0!");
                            x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                        }*/
                        Console.WriteLine(par(x));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "7":
                        Console.WriteLine("Введите значение в градусах:");
                        x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;

                        par = IMath.Cos;
                        /*while (x < 0)
                        {
                            Console.WriteLine("Введите чило больше либо равное 0!");
                            x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                        }*/
                        Console.WriteLine(par(x));
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                    default:
                        Console.WriteLine("Введите операцию или нвжмите Enter, чтобы завершить:");
                        IMath.Menu(chars);
                        str = Console.ReadLine();
                        break;
                }
            }
        }
    }
}
