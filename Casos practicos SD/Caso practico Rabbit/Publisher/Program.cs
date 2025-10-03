using System.Text;
using RabbitMQ.Client;

var factory = new ConnectionFactory() { HostName = "rabbitmq" };
using var connection = factory.CreateConnection();
using var channel = connection.CreateModel();

channel.QueueDeclare(queue: "test_queue",
                     durable: false,
                     exclusive: false,
                     autoDelete: false,
                     arguments: null);

for (int i = 1; i <= 10; i++)
{
    string message = $"Mensaje {i}";
    var body = Encoding.UTF8.GetBytes(message);

    channel.BasicPublish(exchange: "",
                         routingKey: "test_queue",
                         basicProperties: null,
                         body: body);
    Console.WriteLine($"[x] Enviado: {message}");
    System.Threading.Thread.Sleep(500);
}

Console.WriteLine("Presiona Enter para salir...");
Console.ReadLine();
