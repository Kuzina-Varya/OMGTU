using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        List<string> lst1 = new List<string>();
        List<string> lst2 = new List<string>();

        while (true)
        {
            string s = Console.ReadLine();
            if (s == "END")
            {
                break;
            }
            else
            {
                lst1.Add(s);
            }
        }

        for (int i = 0; i < lst1.Count; i++)
        {
            for (int j = i + 1; j < lst1.Count; j++)
            {
                if (lst1[i].Substring(0, 4) == lst1[j].Substring(0, 4))
                {
                    if (lst1[i].Length > lst1[j].Length)
                    {
                        lst1[j] = lst1[i];
                    }
                    else
                    {
                        lst1[i] = lst1[j];
                    }
                }
            }
        }

        string s2 = Console.ReadLine();
        for (int i = 0; i < lst1.Count; i += 2)
        {
            if (s2.Contains(lst1[i]) || lst2.Contains(lst1[i]))
            {
                lst2.Add(lst1[i + 1]);
            }
        }

        lst2 = lst2.OrderBy(x => int.Parse(x.Substring(0, 4))).ToList();
        foreach (string item in lst2)
        {
            if (item.Length < 6)
            {
                Console.WriteLine(item + "Unknown Name");
            }
            else
            {
                Console.WriteLine(item);
            }
        }
    }
}
