namespace _26_12
{
    internal class Program
    {
        static void Main(string[] args)
        {
            for (double n = Math.Round(Math.Sqrt(106732567)); n <= Math.Ceiling(Math.Sqrt(152673836)); n++)
            {
                double maxdel = 0; int cnt = 0;
                for (int i = 2; i < n; i++)
                {
                    if (Math.Pow(n, 2) % i == 0)
                    {
                        maxdel = Math.Pow(n, 2) / i; cnt++;
                    }
                    if (cnt > 1) continue;
                }
                if (cnt == 1)
                {
                    Console.WriteLine(Math.Pow(n, 2) + " : " + maxdel);
                }
            }
            Console.ReadLine();
            // Кузина, Кириченко, Калягина, Иванов, Кондаков
        }
    }
}