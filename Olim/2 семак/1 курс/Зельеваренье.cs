using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        var actions = new List<string>
        {
            "DUST root tooth",
            "WATER 1 tear"
        };

        var spells = new List<string>();
        foreach (var action in actions)
        {
            var parts = action.Split(' ');
            var method = parts[0];
            var ingredients = new List<string>();
            for (int i = 1; i < parts.Length; i++)
            {
                if (int.TryParse(parts[i], out int index))
                {
                    ingredients.Add(spells[index - 1]);
                }
                else
                {
                    ingredients.Add(parts[i]);
                }
            }
            var spell = string.Empty;
            switch (method)
            {
                case "MIX":
                    spell = "MX" + string.Join("", ingredients) + "XM";
                    break;
                case "WATER":
                    spell = "WT" + string.Join("", ingredients) + "TW";
                    break;
                case "DUST":
                    spell = "DT" + string.Join("", ingredients) + "TD";
                    break;
                case "FIRE":
                    spell = "FR" + string.Join("", ingredients) + "RF";
                    break;
            }
            spells.Add(spell);
        }

        Console.WriteLine(spells[spells.Count - 1]);
    }
}
