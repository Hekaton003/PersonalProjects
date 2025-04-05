using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace MobileStore.Models
{
    public class Review
    {
        [Key]
        public int Id { get; set; }

        public DateTime DateTime { get; set; }

        public int rating { get; set; }

        public string Name { get; set; }

        public string Comment { get; set; }

        public int ProductID { get; set; }

        [ForeignKey("ProductID")]
        public virtual Mobile Mobile { get;set;}

        public Review() { }
    }
}