## Project Name:
CoffeeShop

## Project Overview:
CoffeeShop is a django web application that simulates an online coffee shop where users can browse a coffee menu and the detail page of each item in the menu, register, log in, add items to their cart, make online payments, like products, and leave ratings and reviews for products.

## Project Structure:
The project consists of 4 main applications:

1. Users Application:
This application handles user authentication and registration. Users can sign up, log in, and manage their profile page. The registeration will be by using email and password so that demand to customizing user model and use AbstractUser class, also that need from each user to complete registeration by confirmEmail in email to be activate user. also there need OTP code to confirm user mobile number if the user choice to enable_two_factor_authentication.In this application there is need of signals to send confirmation email by uid and token also to create user profile.

2. Pages Application:
The Pages application has no models, it is only responsible for displaying the main application pages for users and admin like index, about, admin dashboard and dashboard chart and another pages.

3. Products Application:
The Products application is responsible for all product(coffee) activity, it is for displaying the coffee menu and coffee details. It includes the following features:
  - All products(products): Display a list of coffee menu contain all products with images, names, descriptions, prices, number of views, likes, ratings and reviews.
  - Search product : Users can search for product according to name,description, price range and the searcher can select if the search be sensitive or unsersetive.
  - Product Details(product): Users can click on a product to view its details, including a larger image, detailed description, and ratings and reviews.
  - The authenticated user can interactive with this product that include:
  - Product Ratings: Users can rate products on a scale (e.g., 1 to 5 stars).
  - Product Reviews: Users can write detailed reviews for product.
  - Product Likes: Users can like product that are interested in and view the favorite products list for himself.
  - Like, rate, wrirte review and add to card after choicing the quantity all in product detaial page activity.

5. Ecommerce Application
The Ecommerce application manages the shopping cart and online payments.It includes the following features: 
Shopping Cart: Users can add products to their cart, adjust quantities, remove items and list the cart items and total price.
Users can create an order by adding item to the cart after decide it's quantity.
Checkout: Users can proceed to checkout, enter shipping information, and make online payments using a payment gateway.



## User Workflow:
User Registration and Authentication:

- Users can register by providing their email, and password.
Registered and activated users can log in to their accounts.

- Browsing Coffee Menu:
Any visitor can browse the coffee menu to view available products also can view product detail page but cannot interactive with it before login in. Each product listing includes an image, name, description, price, and an option to add it to the cart.

- Adding to Cart:
Users can add products to their shopping cart.
They can adjust the quantity of items in the cart and remove items as needed.

- Checkout and Payment:
Users can proceed to checkout from the cart.They provide shipping information and select a payment method.
Payment is processed securely using an online payment gateway (e.g., Stripe).

- Product Interaction:
Users can like or favorite products they are interested in.
Users can rate products on a scale and write review.
Users can create an order by adding item to the cart after decide it's quantity.

## Admin Panel:
An admin panel should be available for managing products, users, and orders.
Admins can add new products, edit and delete existing products, and view orders placed by users.
Admins can view all users,all orders placed by users and interactive with it by changing the order status.
Admins can view the chart to a table or query and customize the chart with a variety of properties.


## Technology Stack:
Django for the backend framework.
HTML, CSS, Bootstrap and JavaScript for the frontend.
Database system like PostgreSQL to store user data, product details, and orders.
Payment gateway integration for online payments (e.g., Stripe).

## Security Considerations:
- Using python-dotenv, It helps to keep the project code secure. By storing the sensitive environment variables in .env file without having to worry about them being accidentally leaked in the applications code.
- Ensure user authentication and authorization for sensitive operations.
- Implement secure payment processing to protect user financial data.
- Validate user input to prevent SQL injection and other security vulnerabilities.
- Regularly update dependencies and apply security patches.

## Testing and Deployment:
Comprehensive testing, including unit tests and user acceptance testing.
Deployment on a production server, with proper web server configuration and security measures.
Consider using a version control system like Git for code management.

## User Experience:
Ensure a responsive and user-friendly design for both desktop and mobile users.
Use user feedback and analytics to continuously improve the user experience by contact us page.

## Documentation:
Provide clear documentation for setting up and running the project, including installation and configuration instructions.
By following this project outline, you can create a functional CoffeeShop Django application that allows users to browse, shop, and interact with coffee products online while maintaining a secure and user-friendly experience.


## System Architecture:
![coffeshop_project](https://github.com/mayals/CoffeeShop_django_v2/assets/48769543/43772f4f-d782-4cb2-bfcf-6573ba242832)


## ER Diagram:
![Coffeeshop_dbdiagram](https://github.com/mayals/CoffeeShop_django_v2/assets/48769543/15f0389e-011b-4676-b276-a001aed6de95)

https://dbdiagram.io/d/Coffeeshop-6505b34302bd1c4a5eb1811a


## Getting Started:
To run CoffeeShop project locally, follow these steps:
1.  Clone the repository: `git clone https://github.com/mayals/CoffeeShop_django_v2.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to 
    connect to your database to be the default database.
6.  Change `.env.templates` to .env and setup you environment variables. 
7.  Set up the database: `python3 manage.py migrate`
8.  Create a superuser account: `python3 manage.py createsuperuser`
9.  Start the development server: `python3 manage.py runserver`
