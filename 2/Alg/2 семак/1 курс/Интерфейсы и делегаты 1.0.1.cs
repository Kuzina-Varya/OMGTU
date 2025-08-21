// See https://aka.ms/new-console-template for more information
interface IMath
{
    public double Sum(double x, double y);
    public double Subtraction(double x, double y);
    public double Multiplication(double x, double y);
    public double Division(double x, double y);
    public double Sqrt(double x);
    public double Sin(double x);
    public double Cos(double x);


}
class Mathematic : IMath
{
    public double x { get; set; } 
    public double y { get; set; }  
    public double Sum(double x, double y)
    {
        return x + y;
    }
    public double Subtraction(double x, double y)
    {
        return x - y;
    }
    public double Multiplication(double x, double y)
    {
        return x * y;
    }
    public double Division(double x, double y)
    {
        return Math.Round(x / y);
    }
    public double Sqrt(double x)
    {
        return Math.Round(Math.Sqrt(x));
    }
    public double Sin(double x)
    {
        return Math.Round(Math.Sin(x));
    }
    public double Cos(double x)
    {
        return Math.Round(Math.Cos(x));//в радианах=>pi/3
    }
    public Mathematic(double x, double y=0.0)
    {
        this.x = x;
        this.y = y;
    }
}
delegate double Parametr(double x);
delegate double Parametrs(double x, double y);
namespace интерфейсы_и_делегаты1
{
    internal class Program
    {
        static void Menu(string[] cars)
        {
            Console.WriteLine("Введите какое действие вы хотите совершить:"); for (int i = 0; i < 7; i++)
            {
                Console.WriteLine($"{i + 1}_ {cars[i]}");
            }
        }
        static void Main(string[] args)
        {
            string[] chars = { "+", "-", "*", "/", "корень", "sin", "cos" };
            Menu(chars);
            Mathematic mathematic;
            string str = Console.ReadLine();
            while (str != null)
            {
                switch (str)
                {
                    case "1":
                        Console.WriteLine("Введите два значения,которые нужно сложить:"); 
                        double x = Convert.ToDouble(Console.ReadLine());
                        double y = Convert.ToDouble(Console.ReadLine());
                        mathematic = new Mathematic(x,y);
                        Parametrs pars = mathematic.Sum; 
                        Console.WriteLine(pars(x, y));
                        Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "2":
                        Console.WriteLine("Введите два значения,где первое-уменьшаемое, второе-вычитаемое:");
                        x = Convert.ToDouble(Console.ReadLine());
                        y = Convert.ToDouble(Console.ReadLine());
                        mathematic = new Mathematic(x, y);
                        pars = mathematic.Subtraction;
                        Console.WriteLine(pars(x, y)); 
                        Menu(chars);
                        str = Console.ReadLine(); 
                        break;
                    case "3":
                        Console.WriteLine("Введите два значения,где первое-множитель1, второе-множитель2:");
                        x = Convert.ToDouble(Console.ReadLine()); 
                        y = Convert.ToDouble(Console.ReadLine());
                        mathematic = new Mathematic(x, y);
                        pars = mathematic.Multiplication;
                        Console.WriteLine(pars(x, y));
                        Menu(chars); 
                        str = Console.ReadLine();
                        break;
                    case "4":
                        Console.WriteLine("Введите два значения,где первое-делимое, второе-делитель:"); 
                        x = Convert.ToDouble(Console.ReadLine());
                        y = Convert.ToDouble(Console.ReadLine());
                        mathematic = new Mathematic(x, y);
                        pars = mathematic.Division;
                        while (y == 0)
                        {
                            Console.WriteLine("Делитель не может быть равено 0!");
                            y = Convert.ToDouble(Console.ReadLine());
                        }
                        Console.WriteLine(pars(x, y));
                        Menu(chars);
                        str = Console.ReadLine();
                        break;
                    case "5":
                        Console.WriteLine("Введите значение,которое больше либо равно 0:");
                        x = Convert.ToDouble(Console.ReadLine());
                        mathematic = new Mathematic(x);
                        Parametr par = mathematic.Sqrt; 
                        while (x < 0)
                        {
                            Console.WriteLine("Введите чило больше либо равное 0!");
                            x = Convert.ToDouble(Console.ReadLine());
                        }
                        Console.WriteLine(par(x));
                        Menu(chars); str = Console.ReadLine();
                        break;
                    case "6":
                        Console.WriteLine("Введите значение в градусах:");
                        x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                        mathematic = new Mathematic(x);
                        par = mathematic.Sin;
                        /* while (x < 0)                         {
                             Console.WriteLine("Введите чило больше либо равное 0!");                             x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                         }*/
                        Console.WriteLine(par(x));
                        Menu(chars); 
                        str = Console.ReadLine();
                        break;
                    case "7":
                        Console.WriteLine("Введите значение в градусах:"); 
                        x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                        mathematic = new Mathematic(x);
                        par = mathematic.Cos;
                        /*while (x < 0)                        {
                            Console.WriteLine("Введите чило больше либо равное 0!");                            x = Math.PI * Convert.ToDouble(Console.ReadLine()) / 180.0;
                        }*/
                        Console.WriteLine(par(x));
                        Menu(chars); str = Console.ReadLine();
                        break;
                    default:
                        Console.WriteLine("Введите операцию или нвжмите Enter, чтобы завершить:"); 
                        Menu(chars);
                        str = Console.ReadLine(); 
                        break;
                }
            }
        }
    }
}