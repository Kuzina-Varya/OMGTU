namespace razvedka
{
    internal class Program
    {
        static void Main(string[] args)
        {
            static void Main(string[] args)
            {
                int n = int.Parse(Console.ReadLine());
                Console.WriteLine(K(n));
            }

            static int K(int n)
            {
                if (n < 3)
                {
                    return 0;
                }
                else if (n == 3)
                {
                    return 1;
                }
                else if (n % 2 == 1)
                {
                    return K(n / 2) + K(n / 2 + 1);
                }
                else
                {
                    return 2 * K(n / 2);
                }
            }
        }
    }
}