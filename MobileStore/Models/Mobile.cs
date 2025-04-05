using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace MobileStore.Models
{
    public class Mobile
    {
        [Key]
        public int ID { get; set; }

        public string Name { get; set; }

        public string Brand { get; set; }

        public string Description { get; set; }

        public string ImageURL { get; set; }

        public int Price { get; set; }

        public string Color { get; set; }

        public int Quantity { get; set; }

        public virtual List<Review> Reviews { get; set; }


        public Mobile(string Name, string Brend, string description, int price, int quantity,string ImageUrl,string Colors)
        {
            this.Name = Name;
            this.Brand = Brend;
            this.Description = description;
            this.ImageURL = ImageUrl;
            this.Color = Colors;
            this.Price = price;
            this.Quantity = quantity;
            this.Reviews = new List<Review>();
        }
        public Mobile()
        {
            this.Reviews = new List<Review>();
        }
    }
    public class MobileReview
    {
        public virtual Mobile Mobile { get; set; }

        public virtual Review Review { get; set;}

        public MobileReview()
        {
            
        }
    }
}