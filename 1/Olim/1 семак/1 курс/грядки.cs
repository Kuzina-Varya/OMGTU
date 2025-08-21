namespace грядки
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int k = 20;
            int l = 7;
            int m = 10;
            int n = 5;
            int summ = 0;

            for (int i = 1; i <= k; i++)
            {
                summ += 2 * l + 2 * n + 2 * m * i;
            }

            Console.WriteLine(summ);
            // Формула:2*(m+n)*k+2*l*k+k*m*(k-1) 
        }
    }
}