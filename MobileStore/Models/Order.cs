using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace MobileStore.Models
{
    public class Order
    {
        [Key]
        public int Id { get; set; }

        public virtual Mobile Mobile { get; set; }

        public string Color { get; set; }

        public int Quantity { get; set; }

        public DateTime Date { get; set; }

        public int CustomerId { get; set; }

        public Order()
        {

        }
    }
}