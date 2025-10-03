using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace RestApiService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class InventoryController : ControllerBase
    {
        private static readonly Dictionary<string, int> Stock = new()
        {
            ["P001"] = 100,
            ["P002"] = 50
        };
        private static readonly object stockLock = new();

        [HttpGet("check/{productId}/{quantity}")]
        public IActionResult CheckStock(string productId, int quantity)
        {
            var available = Stock.TryGetValue(productId, out var stockQty) && stockQty >= quantity;
            return Ok(new { productId, available });
        }

        [HttpPost("order")]
        public IActionResult CreateOrder([FromBody] OrderRequest request)
        {
            if (!Stock.ContainsKey(request.ProductId))
                return BadRequest(new { success = false, message = "Product not found." });

            lock (stockLock)
            {
                if (Stock[request.ProductId] >= request.Quantity)
                {
                    Stock[request.ProductId] -= request.Quantity;
                    return Ok(new { success = true, message = "Order created." });
                }
            }
            return BadRequest(new { success = false, message = "Insufficient stock." });
        }
    }

    public class OrderRequest
    {
        public string ProductId { get; set; } = string.Empty;
        public int Quantity { get; set; }
    }
}
