using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        int n, m;
        var input = Console.ReadLine().Split(' ');
        n = int.Parse(input[0]);
        m = int.Parse(input[1]);

        var gears = new List<Gear>();
        for (int i = 0; i < n; i++)
        {
            input = Console.ReadLine().Split(' ');
            int k = int.Parse(input[0]);
            int rk = int.Parse(input[1]);
            gears.Add(new Gear(k, rk));
        }

        var connections = new List<Tuple<int, int>>();
        for (int i = 0; i < m; i++)
        {
            input = Console.ReadLine().Split(' ');
            int s1 = int.Parse(input[0]);
            int s2 = int.Parse(input[1]);
            connections.Add(new Tuple<int, int>(s1, s2));
        }

        input = Console.ReadLine().Split(' ');
        int z1 = int.Parse(input[0]);
        int z2 = int.Parse(input[1]);

        int v = int.Parse(Console.ReadLine());

        var graph = new Dictionary<int, List<int>>();
        foreach (var connection in connections)
        {
            if (!graph.ContainsKey(connection.Item1))
            {
                graph[connection.Item1] = new List<int>();
            }
            graph[connection.Item1].Add(connection.Item2);
            if (!graph.ContainsKey(connection.Item2))
            {
                graph[connection.Item2] = new List<int>();
            }
            graph[connection.Item2].Add(connection.Item1);
        }

        var visited = new HashSet<int>();
        var directions = new Dictionary<int, int>();
        var speeds = new Dictionary<int, double>();
        if (!Dfs(graph, visited, directions, speeds, z1, z1, v, 1,gears))
        {
            Console.WriteLine(-1);
            return;
        }

        Console.WriteLine(1);
        Console.WriteLine(directions[z2]);
        Console.WriteLine(speeds[z2].ToString("F3"));
    }

    static bool Dfs(Dictionary<int, List<int>> graph, HashSet<int> visited, Dictionary<int, int> directions, Dictionary<int, double> speeds, int current, int parent, int direction, double speed, List<Gear> gears)
    {
        visited.Add(current);
        directions[current] = direction;
        speeds[current] = speed;

        foreach (var neighbor in graph[current])
        {
            if (neighbor == parent)
            {
                continue;
            }

            if (visited.Contains(neighbor))
            {
                if (directions[neighbor] != -direction)
                {
                    return false;
                }

                if (speeds[neighbor] != speed * gears[current - 1].Teeth / gears[neighbor - 1].Teeth)
                {
                    return false;
                }
            }
            else
            {
                if (!Dfs(graph, visited, directions, speeds, neighbor, current, -direction, speed * gears[current - 1].Teeth / gears[neighbor - 1].Teeth,gears))
                {
                    return false;
                }
            }
        }

        return true;
    }
}

class Gear
{
    public int Number { get; }
    public int Teeth { get; }

    public Gear(int number, int teeth)
    {
        Number = number;
        Teeth = teeth;
    }
}