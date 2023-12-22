namespace итенсификация_производства
{
    internal class Program
    {
        static void Main(string[] args)
        {
            DateTime date1 = new DateTime(2002, 5, 12);
            DateTime date2 = new DateTime(2002, 5, 15);
            TimeSpan delta = date2 - date1;
            int P = Convert.ToInt32(Console.ReadLine());
            int sum = 0;
            if (1 <= delta.Days && delta.Days < 60000)
            {
                if (0 <= P)
                {
                    if (P <= 5000)
                    {
                        for (int n = 0; n <= delta.Days; n++)
                        {
                            sum += P;
                            P += 1;
                            Console.WriteLine(P + " " + sum);
                        }
                    }
                }
            }
            Console.WriteLine(sum);
        }
    }
}