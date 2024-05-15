// See https://aka.ms/new-console-template for more information

using System;

public class MainClass
{
    public static void Main()
    {
        int n = Convert.ToInt32(Console.ReadLine());
        int i = 1;
        int max_i = 10000000;
        double max_pm = 10000000;
        while (i<=n)
        {
            string k = Console.ReadLine();
            string[] array = k.Split(' ');
            double x1 = Convert.ToDouble(array[0]);
            double y1 = Convert.ToDouble(array[1]);
            double z1 = Convert.ToDouble(array[2]);
            double x2 = Convert.ToDouble(array[3]);
            double y2 = Convert.ToDouble(array[4]);
            double z2 = Convert.ToDouble(array[5]);

            string c1 = array[6];
            string[] c1_0 = c1.Split('.');
            double c1_1 = Convert.ToInt32(c1_0[0]) + Convert.ToInt32(c1_0[1])*0.01;
            
            string c2 = array[7];
            string[] c2_0 = c2.Split('.');
            double c2_1 = Convert.ToInt32(c2_0[0]) + Convert.ToInt32(c2_0[1]) * 0.01;

            double V1 = x1 * y1 * z1;
            double V2 = x2 * y2 * z2;
            double S1 = 2 * (x1 * y1 + x1 * z1 + z1 * y1);
            double S2 = 2 * (x2 * y2 + x2 * z2 + z2 * y2);

            double pm = Math.Abs(S1 * c2_1 - S2 * c1_1) / Math.Abs(S1 * V2 - S2 * V1) * 1000;

            if (pm < max_pm)
            {
                max_i = i;
                max_pm = pm;
            }
            i++;



            Console.WriteLine($"{max_i} {max_pm}");
        }
        
    }
}
