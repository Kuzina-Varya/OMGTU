using System;
using System.Collections.Generic;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        StreamReader file = new StreamReader(@"test.txt");

        string for_func;

        string[] words = { "" };

        while (words.Length != 0)
        {
            try
            {
                words = file.ReadLine().Split();
            }
            catch
            {
                break;
            }
            for_func = "";
            foreach (string word in words)
                for_func += func(word);
            func2(for_func.Split());
            Console.WriteLine();
        }

        file.Close();
    }

    static string func(string word)
    {
        string line = "";
        List<char> list = new List<char>();
        if (word.Length % 2 != 0)
        {
            list.Add(word[word.Length / 2]);
            for (int i = (word.Length - 1) / 2; i >= 1; i--)
            {
                list.Add(word[i - 1]);
                list.Add(word[word.Length - i]);
            }
        }
        else
        {
            for (int i = word.Length / 2; i >= 1; i--)
            {
                list.Add(word[word.Length - i]);
                list.Add(word[i - 1]);
            }
        }
        list.Add(' ');
        foreach (char c in list)
            line += c;
        return line;
    }

    static void func2(string[] words)
    {
        if (words.Length % 2 != 0)
        {
            for (int i = (words.Length - 1) / 2; i >= 1; i--)
            {
                Console.Write(words[i - 1]);
                Console.Write(' ');
                Console.Write(words[words.Length - i]);
                Console.Write(' ');
            }
        }
        else
        {
            for (int i = words.Length / 2; i >= 1; i--)
            {
                Console.Write(words[words.Length - i]);
                Console.Write(' ');
                Console.Write(words[i - 1]);
                Console.Write(' ');
            }
        }
    }
}