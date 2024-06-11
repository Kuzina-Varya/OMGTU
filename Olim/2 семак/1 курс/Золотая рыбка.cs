using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        int n = int.Parse(Console.ReadLine());
        var words = new HashSet<string>();
        for (int i = 0; i < n; i++)
        {
            words.Add(Console.ReadLine());
        }

        int f = int.Parse(Console.ReadLine());
        var firstLetters = new Dictionary<char, int>();
        for (int i = 0; i < f; i++)
        {
            var parts = Console.ReadLine().Split(' ');
            char c = parts[0][0];
            int k = int.Parse(parts[1]);
            firstLetters[c] = k;
        }

        int l = int.Parse(Console.ReadLine());
        var lastLetters = new Dictionary<char, int>();
        for (int i = 0; i < l; i++)
        {
            var parts = Console.ReadLine().Split(' ');
            char c = parts[0][0];
            int k = int.Parse(parts[1]);
            lastLetters[c] = k;
        }

        int count = 0;
        var usedWords = new HashSet<string>();
        foreach (var word in words)
        {
            if (firstLetters.ContainsKey(word[0]) && lastLetters.ContainsKey(word[word.Length - 1]) && !usedWords.Contains(word))
            {
                int firstLetterCount = firstLetters[word[0]];
                int lastLetterCount = lastLetters[word[word.Length - 1]];
                int minCount = Math.Min(firstLetterCount, lastLetterCount);
                count += minCount;
                firstLetters[word[0]] -= minCount;
                lastLetters[word[word.Length - 1]] -= minCount;
                usedWords.Add(word);
            }
        }

        Console.WriteLine(count);
    }
}