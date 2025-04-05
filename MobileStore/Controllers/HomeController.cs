using MobileStore.Models;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.UI.WebControls;

namespace MobileStore.Controllers
{
    public class HomeController : Controller
    {
        private ApplicationDbContext db = new ApplicationDbContext();

        [AllowAnonymous]
        public ActionResult Index()
        {
            var mobiles = db.Mobiles.ToList();
            if (mobiles == null) { 
            return View();
            }else{
                return View(mobiles);
            }
        }
        [HttpGet]
        public JsonResult AutoCompleteSearch(string term)
        {
            var products = db.Mobiles
                             .Where(m => m.Name.Contains(term))
                             .Select(m => new {id = m.ID,value=m.Name})
                             .ToList();

            return Json(products, JsonRequestBehavior.AllowGet);
        }
        [HttpGet]
        public ActionResult FilterProducts(string brand, string price)
        {
            var products = db.Mobiles.AsQueryable();

            if (!string.IsNullOrEmpty(brand) && brand != "All")
            {
                products = products.Where(p => p.Brand == brand);
            }

            if (price == "high")
            {
                products = products.OrderByDescending(p => p.Price);
            }
            else if (price == "low")
            {
                products = products.OrderBy(p => p.Price);
            }

            return PartialView("ProductList", products.ToList());
        }
        public ActionResult Details(int id)
        {
            var mobile = db.Mobiles.Include(m => m.Reviews).FirstOrDefault(m => m.ID == id);
            Customer customer = Session["Customer"] as Customer;
            if (mobile == null)
            {
                return HttpNotFound();
            }
            Review review = new Review();
            review.ProductID = id;
            review.Name = customer.Name;
            review.DateTime = DateTime.Now;
            var mobileReview = new MobileReview
            {
                Mobile = mobile,
                Review = review// Create an empty review object
            };

            return View(mobileReview);
        }

        [HttpPost]
        public ActionResult AddMobiles(int id,string color)
        {
            List<Order> orders = (List<Order>)Session["Orders"];
            Customer customer = (Customer)Session["Customer"];
            Mobile mobile = db.Mobiles.Find(id);
            Order order = new Order
            {
                Mobile = mobile,
                CustomerId = customer.Id,
                Date = DateTime.Now,
                Quantity = 1,
                Color = color
            };

            Order existingItem = orders.FirstOrDefault(m => m.Mobile.ID== order.Mobile.ID);
            if (existingItem != null)
            {
                existingItem.Quantity += 1;
            }
            else
            {
                orders.Add(order);
            }

            Session["Orders"] = orders;
            return RedirectToAction("AddToCart");
        }

        public ActionResult AddToCart()
        {
            List<Order> orders = (List<Order>)Session["Orders"];
            return View(orders);
        }
        [HttpPost]
        public JsonResult UpdateCartQuantity(int index, int quantity)
        {
            List<Order> orders = Session["Orders"] as List<Order>;
            if (orders != null && index >= 0 && index < orders.Count)
            {
                // Update the quantity of the order at the specified index
                orders[index].Quantity = quantity;

                // Update the session with the modified order list
                Session["Orders"] = orders;
                return Json(new { success = true });
            }

            return Json(new { success = false, message = "Invalid order index or session data." });
        }

        public ActionResult RemoveFromCart(int index)
        {
            List<Order> orders = Session["Orders"] as List<Order>;
            Order order = orders[index];
            if (order != null)
            {
                orders.RemoveAt(index);
            }
            Session["Orders"]= orders;
            return RedirectToAction("AddToCart");
        }
        [HttpPost]
        public ActionResult SaveOrder()
        {
            // Retrieve orders from session
            List<Order> orders = (List<Order>)Session["Orders"];

            if (orders == null || !orders.Any())
            {
                return RedirectToAction("Index", "Home");
            }

            // Find the customer using the current DbContext instance
            Customer customer = db.Customers.Find(orders[0].CustomerId);

            if (customer == null)
            {
                // Handle case where the customer is not found
                return RedirectToAction("Index", "Home");
            }

            foreach (var order in orders)
            {
                // Detach the existing order to prevent tracking issues
                db.Entry(order).State = EntityState.Detached;

                // Reattach the mobile entity to the current DbContext instance
                order.Mobile = db.Mobiles.Find(order.Mobile.ID);

                // Re-create the order to be tracked by the current DbContext instance
                Order newOrder = new Order
                {
                    Mobile = order.Mobile,
                    CustomerId = order.CustomerId,
                    Date = order.Date,
                    Quantity = order.Quantity,
                    Color = order.Color,
                };

                // Add the new order to the customer's orders
                customer.Orders.Add(newOrder);
            }

            // Update the customer's orders
            db.Entry(customer).State = EntityState.Modified;

            // Save changes to the database
            db.SaveChanges();

            // Clear the orders from the session
            Session["Orders"] = new List<Order>();

            // Redirect to the home page or any other relevant page
            return RedirectToAction("Index", "Home");
        }

        [HttpPost]
        public ActionResult AddReview(MobileReview model)
        {
            if (ModelState.IsValid)
            {
                Mobile mobile = db.Mobiles.Find(model.Review.ProductID);
                Review review = model.Review;
                review.DateTime = DateTime.Now;
                mobile.Reviews.Add(review);
                db.Entry(mobile).State = EntityState.Modified;
                db.SaveChanges();
                return RedirectToAction("Details", new { id = mobile.ID });
            }
            return View(model);
        }

        public ActionResult Delete(int id)
        {
            var mobile = db.Mobiles.Find(id);
            if (mobile == null)
            {
                return HttpNotFound();
            }
            db.Mobiles.Remove(mobile);
            db.SaveChanges();
            return RedirectToAction("Index");
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
        [HttpPost]
        public ActionResult Contact(ContactFormViewModel model)
        {
            if (ModelState.IsValid)
            {
                // Process the form (e.g., send email, store data, etc.)
                // For demonstration, you might want to add logic to send an email.
                // Replace with actual implementation.

                // Example: Sending an email
                // EmailService.SendEmail(model.Name, model.Email, model.Subject, model.Message);

                TempData["Message"] = "Your message has been sent successfully!";
                return RedirectToAction("Index", "Home"); // Redirect to a thank-you page or home page
            }

            // If the model is not valid, return the view with validation errors
            return View(model);
        }

        public ActionResult Edit(int id)
        {
            Mobile mobile = db.Mobiles.Find(id);
            return View(mobile);
        }
        [HttpPost]
        public ActionResult Edit(Mobile mobile)
        {
            if (ModelState.IsValid)
            {
                db.Entry(mobile).State = EntityState.Modified;
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(mobile);
        }
        public ActionResult Product()
        {
            Mobile mobile = new Mobile();
            return View(mobile);
        }
        [HttpPost]
        public ActionResult Product(Mobile model)
        {
            if (ModelState.IsValid)
            {
                db.Mobiles.Add(model);
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            else { return View(model); }
        }
    }
}