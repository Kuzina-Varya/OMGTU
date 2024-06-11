using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        var cities = new HashSet<string>();
        var firstLetters = new Dictionary<char, List<string>>();
        var lastLetters = new Dictionary<char, List<string>>();

        string city=Console.ReadLine();
        while ((city != ""))
        {
            cities.Add(city);
            if (!firstLetters.ContainsKey(city[0]))
            {
                firstLetters[city[0]] = new List<string>();
            }
            firstLetters[city[0]].Add(city);
            if (!lastLetters.ContainsKey(city[city.Length - 1]))
            {
                lastLetters[city[city.Length - 1]] = new List<string>();
            }
            lastLetters[city[city.Length - 1]].Add(city);
            city=Console.ReadLine();
        }

        var chainLengths = new List<int>();
        while (cities.Count > 0)
        {
            var chain = new HashSet<string>();
            var currentCity = cities.First();
            chain.Add(currentCity);
            cities.Remove(currentCity);
            var firstLetter = currentCity[0];
            var lastLetter = currentCity[currentCity.Length - 1];

            while (true)
            {
                if (lastLetters.ContainsKey(firstLetter))
                {
                    var nextCity = lastLetters[firstLetter].FirstOrDefault(c => !chain.Contains(c));
                    if (nextCity == null)
                    {
                        break;
                    }
                    chain.Add(nextCity);
                    cities.Remove(nextCity);
                    firstLetter = nextCity[0];
                    lastLetter = nextCity[nextCity.Length - 1];
                }
                else
                {
                    break;
                }
            }

            while (true)
            {
                if (firstLetters.ContainsKey(lastLetter))
                {
                    var nextCity = firstLetters[lastLetter].FirstOrDefault(c => !chain.Contains(c));
                    if (nextCity == null)
                    {
                        break;
                    }
                    chain.Add(nextCity);
                    cities.Remove(nextCity);
                    firstLetter = nextCity[0];
                    lastLetter = nextCity[nextCity.Length - 1];
                }
                else
                {
                    break;
                }
            }

            chainLengths.Add(chain.Count);
        }

        Console.WriteLine(chainLengths.Count);
        foreach (var length in chainLengths.OrderByDescending(l => l))
        {
            Console.WriteLine(length);
        }
    }
}