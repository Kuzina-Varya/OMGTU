namespace стэк_со_скобками
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string str = Console.ReadLine();
            Stack<string> stack = new Stack<string>();
            while (str.Length > 0)
            {
                if (stack.Count > 0)
                {
                    stack.Pop();
                }

                string sabsatr = str.Substring(0, 2);
                str = str.Remove(0, 2);
                stack.Push(sabsatr);
                if ((stack.Contains("()")) || (stack.Contains("{}")) || (stack.Contains("[]")))
                {
                    continue;
                }

                else
                {
                    Console.WriteLine("Скобки поставлены неправильно");
                    break;
                }


            }
        }
    }
}
