using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace MobileStore.Models
{
    public class Customer
    {
        [Key]
        public int Id { get; set; }

        [Required(ErrorMessage = "Name and Surname Required!!!")]
        [Display(Name = "Name and Surname:")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Phone Required!!!")]
        [Display(Name = "Phone:")]
        public string Phone { get; set; }

        [Required(ErrorMessage = "Address Required!!!")]
        [Display(Name = "Address:")]
        public string Address { get; set; }

        [Required]
        [StringLength(100, ErrorMessage = "The {0} must be at least {2} characters long.", MinimumLength = 6)]
        [DataType(DataType.Password)]
        [Display(Name = "Password")]
        public string Password { get; set; }

        [Required]
        [EmailAddress]
        [Display(Name = "Email: ")]
        public string Email { get; set; }

        [Required]
        [Display(Name = "Country: ")]
        public string Country { get; set; }

        [Required]
        [Display(Name = "City: ")]
        public string City { get; set; }

        [Required]
        [Display(Name = "PostalCode: ")]
        public string PostalCode { get; set; }

        public virtual List<Order> Orders { get; set; }

        public Customer(string name, string phone, string address, string password, string email, string country, string city, string postalCode)
        {
            this.Name = name;
            this.Phone = phone;
            this.Address = address;
            this.Password = password;
            this.Email = email;
            this.Country = country;
            this.City = city;
            this.PostalCode = postalCode;
            this.Orders = new List<Order>();
        }
        public Customer() {
            this.Orders = new List<Order>();
        }
    }
    
}