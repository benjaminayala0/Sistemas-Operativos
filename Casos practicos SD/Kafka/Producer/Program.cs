using System;
using System.Threading.Tasks;
using Confluent.Kafka;

var config = new ProducerConfig { BootstrapServers = "localhost:9092" };
using var producer = new ProducerBuilder<Null, string>(config).Build();

for (int i = 1; i <= 10; i++)
{
    var message = $"Mensaje {i}";
    var result = await producer.ProduceAsync("test_topic", new Message<Null, string> { Value = message });
    Console.WriteLine($"Enviado: {message} a {result.TopicPartitionOffset}");
    await Task.Delay(500);
}

Console.WriteLine("Presiona Enter para salir...");
Console.ReadLine();
