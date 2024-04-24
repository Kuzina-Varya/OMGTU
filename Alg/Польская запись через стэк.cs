using System.Text.RegularExpressions;
using System.Text;
using System.Collections.Generic;
using System.Threading.Channels;
namespace польская_запись_через_стэк
{

    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("ВВОДИТЕ ВСЕ ОПЕРАЦИИ(УМНОЖЕНИЕ ТОЖЕ)");
            StringBuilder myStringBuilder = new StringBuilder(Console.ReadLine());
            myStringBuilder.Replace(',', '0');
            myStringBuilder.Replace('(', '0');
            myStringBuilder.Replace(')', '0');
            Stack<int> values = new Stack<int>();
            int count = 0;
            for (int i = 0; i < myStringBuilder.Length; i++)
            {
                if (((myStringBuilder[i] != '/') && (myStringBuilder[i] != '*') && (myStringBuilder[i]) != '-') && (myStringBuilder[i] != '+') && (myStringBuilder[i] != '^') && (myStringBuilder[i] != ')') && (myStringBuilder[i] != '(') && (myStringBuilder[i] != '0'))
                {
                    values.Push((int)(Char.GetNumericValue(myStringBuilder[i])));
                }
                else
                {
                    if (myStringBuilder[i]!='0') count++;
                   

                    if ((values.Count >= 2))
                    {
                        int a = values.Pop();
                        int b = values.Pop();
                        switch (myStringBuilder[i])
                        {
                            case '/':
                                if (a == 0) Console.WriteLine(" Делить на ноль неприлично... ");

                                values.Push(b / a);
                                break;
                            case '*':
                                values.Push((b * a));
                                break;
                            case '-':
                                values.Push(b - a);
                                break;
                            case '+':
                                values.Push(b + a);
                                break;
                            case '^':
                                values.Push(Convert.ToInt32(Math.Pow(Convert.ToDouble(b), Convert.ToDouble(a))));
                                break;
                            default:
                                values.Push(b);
                                values.Push(a);
                                break;


                        }
                    }



                }

            }
            
            Console.WriteLine(values.Pop());

        }
    }
}





