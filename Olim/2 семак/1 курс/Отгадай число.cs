using System.Security.Cryptography;

class Program
{
    static void Main()
    {
        int n = int.Parse(Console.ReadLine());
        int lin = 0;
        int count_x = 1;
        for (int i = 0; i < n; i++)
        {
            string[] s = Console.ReadLine().Split(' ', 2);
            switch (s[0])
            {
                case "+":
                    if (s[1] != "x")
                        lin += int.Parse(s[1]);
                    else
                        count_x++;
                    break;
                case "-":
                    if (s[1] != "x")
                        lin -= int.Parse(s[1]);
                    else count_x--;
                    break;
                case "*":
                    lin *= int.Parse(s[1]);
                    count_x *= int.Parse(s[1]);
                    break;
            }
        }
        int rezult = int.Parse(Console.ReadLine());
        rezult -= lin;
        Console.WriteLine(rezult /= count_x);
    }
}
