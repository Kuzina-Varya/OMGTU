using System;
using System.IO;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        var file = new StreamReader("input.txt");

        var branches = new List<int[]>();
        var apples = new List<int[]>();

        var tree = Array.ConvertAll(file.ReadLine().Split(" "), int.Parse);

        for (int i = 0; i < tree[0]; i++)
            branches.Add(Array.ConvertAll(file.ReadLine().Split(" "), int.Parse));

        for (int i = 0; i < tree[1]; i++)
            apples.Add(Array.ConvertAll(file.ReadLine().Split(" "), int.Parse));

        var worm = Array.ConvertAll(file.ReadLine().Split(" "), int.Parse);

        for (int i = 0; i < apples.Count; i++)
        {
            if (apples[i][1] < worm[1])
                apples.RemoveAt(i);
        }

        int[,] mat = new int[tree[0] + 1, tree[0] + 1];

        int c = 1;
        for (int i = 0; i < branches.Count; i++)
        {
            mat[branches[i][0], c] = branches[i][1];
            mat[c, branches[i][0]] = branches[i][1];
            c++;
        }

        for (int k = 0; k < tree[0] + 1; k++)
        {
            for (int i = 0; i < tree[0] + 1; i++)
            {
                for (int j = 0; j < tree[0] + 1; j++)
                {
                    if (mat[i, k] != 0 && mat[k, j] != 0)
                    {
                        int newDist = mat[i, k] + mat[k, j];
                        if (mat[i, j] == 0 || newDist < mat[i, j])
                            mat[i, j] = newDist;
                    }
                }
            }
        }

        

        var totalDist = 0;
        var that = worm[0];

        while (apples.Count != 0)
        {
            (int ans, int th) = func(that, totalDist, mat, apples);
            that = th;
            totalDist = ans;
        }
        Console.WriteLine(totalDist);
    }

    static (int, int[]) help(int that, int[,] mat, List<int[]> apples)
    {
        var mas = new int[apples.Count];

        for (int i = 0; i < apples.Count; i++)
            mas[i] = mat[that, apples[i][0]];

        var min = mas[0];
        var id = 0;

        for (int i = 1; i < mas.Length; i++)
        {
            if (min > mas[i])
            {
                min = mas[i];
                id = i;
            }
        }
        return (that, apples[id]);
    }

    static (int, int) func(int that, int totalDist, int[,] mat, List<int[]> apples)
    {
        (int th, int[] next) = help(that, mat, apples);
        totalDist += mat[th, next[0]];
        apples.Remove(next);
        return (totalDist, next[0]);
    }
}