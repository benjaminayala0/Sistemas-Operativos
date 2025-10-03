using System;
using System.Threading;
using Confluent.Kafka;

var config = new ConsumerConfig
{
    GroupId = "test-group",
    BootstrapServers = "localhost:9092",
    AutoOffsetReset = AutoOffsetReset.Earliest
};

using var consumer = new ConsumerBuilder<Ignore, string>(config).Build();
consumer.Subscribe("test_topic");

CancellationTokenSource cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cts.Cancel(); };

try
{
    while (true)
    {
        var cr = consumer.Consume(cts.Token);
        Console.WriteLine($"Recibido: {cr.Message.Value}");
    }
}
catch (OperationCanceledException)
{
    consumer.Close();
}
