namespace krestyanin
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int Max = int.Parse(Console.ReadLine());
            int total = 0;
            for (int j = 1; j <= Max; j++)
            {
                for (int i = 2; i <= 17; i++)
                {
                    if (j % (int)Math.Pow(2, i) - 1 == 0)
                    {
                        total += 1;
                    }
                }
            }
            int res = Max + total;
            Console.WriteLine(res);
        }
    }
}