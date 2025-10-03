using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        var baseUrl = Environment.GetEnvironmentVariable("API_BASE") ?? "http://localhost:5000/";
        using var client = new HttpClient { BaseAddress = new Uri(baseUrl) };
        Console.WriteLine($"Usando API en {baseUrl}");

        // Check stock
        var check = await client.GetFromJsonAsync<CheckResponse>("api/inventory/check/P001/3");
        Console.WriteLine($"Check: product={check.ProductId} available={check.Available}");

        // Create order
        var orderReq = new OrderRequest { ProductId = "P001", Quantity = 3 };
        var orderResp = await client.PostAsJsonAsync("api/inventory/order", orderReq);
        var orderRes = await orderResp.Content.ReadFromJsonAsync<OrderResult>();
        Console.WriteLine($"Order result: success={orderRes.Success} message={orderRes.Message}");
    }

    public class CheckResponse { public string ProductId { get; set; } public bool Available { get; set; } }
    public class OrderRequest { public string ProductId { get; set; } public int Quantity { get; set; } }
    public class OrderResult { public bool Success { get; set; } public string Message { get; set; } }
}
