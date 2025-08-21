using System;
using System.Collections.Generic;
using System.Linq;

public class CallData
{
    public string CallerNumber { get; set; }
    public string ReceiverNumber { get; set; }
    public DateTime CallDate { get; set; }
    public int DurationMinutes { get; set; }
}

public class Program
{
    public static void Main(string[] args)
    {

        var callDataList = new List<CallData>
        {
            new CallData { CallerNumber = "1234567890", ReceiverNumber = "9876543210", CallDate = new DateTime(2022, 1, 1), DurationMinutes = 10 },
            new CallData { CallerNumber = "1234567890", ReceiverNumber = "5555555555", CallDate = new DateTime(2022, 1, 2), DurationMinutes = 20 },
            new CallData { CallerNumber = "1234567890", ReceiverNumber = "9876543210", CallDate = new DateTime(2022, 1, 3), DurationMinutes = 15 },
            new CallData { CallerNumber = "0987654321", ReceiverNumber = "1234567890", CallDate = new DateTime(2022, 1, 1), DurationMinutes = 5 },

        };


        string selectedNumber = "1234567890";


        var callsByDate = callDataList
            .Where(cd => cd.CallerNumber == selectedNumber)
            .GroupBy(cd => cd.CallDate)
            .Select(g => new { CallDate = g.Key, MostCalledNumber = g.GroupBy(cd => cd.ReceiverNumber).OrderByDescending(gg => gg.Count()).First().Key })
            .OrderBy(g => g.CallDate);

        Console.WriteLine($"Кому чаще всего звонил {selectedNumber}:");
        foreach (var call in callsByDate)
        {
            Console.WriteLine($"{call.CallDate.ToShortDateString()}: {call.MostCalledNumber}");
        }


        var callsByDuration = callDataList
            .GroupBy(cd => cd.CallerNumber)
            .Select(g => new
            {
                CallerNumber = g.Key,
                MostCalledNumbers = g.GroupBy(cd => cd.ReceiverNumber)
                    .Select(gg => new
                    {
                        ReceiverNumber = gg.Key,
                        TotalDuration = gg.Sum(cd => cd.DurationMinutes)
                    })
                    .OrderByDescending(gg => gg.TotalDuration)
            });

        Console.WriteLine("С кем дольше всего разговаривал каждый из абонентов:");
        foreach (var caller in callsByDuration)
        {
            Console.WriteLine($"Звонящий: {caller.CallerNumber}");
            foreach (var call in caller.MostCalledNumbers)
            {
                Console.WriteLine($"{call.ReceiverNumber}: {call.TotalDuration} минут");
            }
            Console.WriteLine();
        }
    }
}
