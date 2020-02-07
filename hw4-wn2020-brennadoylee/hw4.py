
import random
import unittest

## Name : Brenna Doyle
## People you worked with :
## Github URL : https://github.com/SI206-UMich/hw4-wn2020-brennadoylee




### Customer Class
class Customer:

    # Constructor
    def __init__(self, name, money = 50):
        self.name = name
        self.money = money

    # Deposits money_top_add into customers account.
    def deposit_money(self, money_to_add):
        self.money += money_to_add


    # Pays the ComidaExpress driver 
    def make_payment(self, driver, amount):
        self.money -= amount
        receive_payment(self.driver)
        
    
    '''
    
    def test_make_payment(self):
        # Check to see how much money there is prior to a payment
        previous_money_customer = self.c2.money
        previous_money_driver = self.d2.money

        # Make the payment
        self.c2.make_payment(self.d2, 30)

        # See if money has changed hands
        self.assertEqual(self.c2.money, previous_money_customer - 30)
        self.assertEqual(self.d2.money, previous_money_driver + 30)
'''
    # Orders food from the restaurant to be delivered by the driver,
    # assuming certain conditions are met.  
    def order_food(self, driver, restaurant):
        if not(driver.know_restaurant(restaurant)):
            print("Sorry, this driver doesn't know that restaurant. Please try a different restaurant!")
        elif self.money < driver.estimated_cost(restaurant):
            print("Don't have enough money for that :( Please try a different restaurant!")
        elif not(restaurant.has_food()):
            print("Restaurant has run out of food :( Please try a different restaurant!")
        else:
            bill = driver.place_order(restaurant)
            self.make_payment(driver, bill)
            self.eat_food()

    # Eats the delivered food and prints out a message to indicate this.        
    def eat_food(self):
        print("That was yummy!")

    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.money) + "and I am starving!"

### comidaExpress Driver Class
class Driver:

    # Constructor. 
    def __init__(self, name, money = 500, restaurants = [], delivery_fee = 5):
        self.name = name
        self.money = money
        self.restaurants = restaurants[:] # makes a copy of the list
        self.delivery_fee = delivery_fee

    # Adds a restaurant to driver's known list of restaurants   
    def add_restaurant(self, new_restaurant):
        self.restaurants.append(new_restaurant)

    # Receives payment from customer, and adds the money to the driver's account. 
    def receive_payment(self, money):
        self.money += money 

    # Returns the estimated cost of a delivery, namely the cost of the restaurant
    # plus the driver's own delivery fee.   
    def estimated_cost(self, restaurant):
        return restaurant.cost + self.delivery_fee

    # Places an order at the restaurant.
    # The delivery driver pays the restaurant the cost.
    # The restaurant processes the order
    # Function returns cost of the food + delivery fee.
    def place_order(self, restaurant):
        self.money = self.money - restaurant.cost 
        restaurant.process_order()
        return self.estimated_cost(restaurant)

    # Returns boolean value letting customer know if this driver can deliver to a restaurant or not.    
    def know_restaurant(self, restaurant):
        return restaurant in self.restaurants 

    # string function.  
    def __str__(self):
        return "Hello, my name is " + self.name + "I am an comidaExpresseats driver, who has saved up " + str(self.money) + ". I charge $" + str(self.delivery_fee) + " and I can deliver from " + str(len(self.restaurants)) + " restaurants."


### Create Restaurant class here
class Restaurant:
    def __init__(self, name, money = 500, cost = 10, food_left = 10):
        self.name = name
        self.money = money
        self.cost = cost
        self.food_left = food_left

    def process_order(self, cost):
        self.food_left -= 1
        self.money += cost
    
    def has_food(self):
        if self.food_left != 0:
            return True
    
    def stock_up(self, amount, cost):
        if self.money > cost * amount:
            self.money -= cost
            self.food_left += amount
    
    def __str__(self):
        return "Hello, we are {}. It costs us {} to make a meal. We have {} food left in stock, and we have {} money in total.".format(self.restaurant, self.cost, self.food_left, self.money)
  
class TestAllMethods(unittest.TestCase):

    def setUp(self):
        self.c1 = Customer("Brenna")
        self.c2 = Customer("Alana", 200)
        self.r1 = Restaurant("Savas")
        self.r2 = Restaurant("Taco Bell", cost = 5, food_left = 100)
        self.r3 = Restaurant("Panera", cost = 15)
        self.d1 = Driver("Jimmy")
        self.d2 = Driver("Sean", delivery_fee = 10, restaurants = [self.r1, self.r2])

    ## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.c1.name, "Brenna")
        self.assertEqual(self.c2.name, "Alana")
        self.assertEqual(self.c1.money, 50)
        self.assertEqual(self.c2.money, 200)

    ## Check to see whether constructors work
    def test_driver_constructor(self):
        self.assertEqual(self.d1.name, "Jimmy") 
        self.assertEqual(self.d1.delivery_fee, 5)
        self.assertEqual(self.d2.delivery_fee, 10)
        self.assertEqual(self.d1.restaurants, [])
        self.assertEqual(len(self.d2.restaurants), 2)

    ## Check to see whether constructors work
    def test_restaurant_constructor(self):
        self.assertEqual(self.r1.name, "Savas")
        self.assertEqual(self.r1.money, 500)
        self.assertEqual(self.r1.food_left, 10)
        self.assertEqual(self.r2.food_left, 100)
        self.assertEqual(self.r3.cost, 15)

    # Check that restaurant can stock up properly.
    def test_stocking_food(self):
        r4 = Restaurant("Coney", food_left = 5, money = 53, cost = 5)
        
        # Testing whether restaurant can stock up on food   
        self.assertEqual(r4.food_left, 5)
        r4.stock_up(10)
        self.assertEqual(r4.food_left, 15)
        self.assertEqual(r4.money, 3)

        # Testing whether restaurant doesn't stock up on food
        # when it doesn't have enough money.
        r4.stock_up(9)
        self.assertEqual(r4.food_left, 15)
        self.assertEqual(r4.money, 3)

    def test_make_payment(self):
        # Check to see how much money there is prior to a payment
        previous_money_customer = self.c2.money
        previous_money_driver = self.d2.money

        # Make the payment
        self.c2.make_payment(self.d2, 30)

        # See if money has changed hands
        self.assertEqual(self.c2.money, previous_money_customer - 30)
        self.assertEqual(self.d2.money, previous_money_driver + 30)


    # Check to see that comidaExpress driver can manage restaurants properly
    # (i.e., that add_restaurant and know_restaurant work)
    def test_adding_and_knowing_restaurants(self):
        d3 = Driver("Grant", delivery_fee = 10, restaurants = [self.r1, self.r2])
        self.assertTrue(d3.know_restaurant(self.r1))
        self.assertFalse(d3.know_restaurant(self.r3))
        d3.add_restaurant(self.r3)
        self.assertTrue(d3.know_restaurant(self.r3))
        self.assertEqual(len(d3.restaurants), 3)


    # Test that estimated cost works properly.
    def test_estimated_cost(self):
        self.assertEqual(self.d1.estimated_cost(self.r1), 0)
        self.assertEqual(self.d2.estimated_cost(self.r2), 221)


    # Check that restaurant can properly see when it is empty
    def test_has_food(self):        
		#new restaurant instance
		self.r5 = Restaurant("Chipotle", food_left =3)
		self.r6 = Restaurant("Joe's Pizza", food_left = 0)
        # Test to see if has_food returns True when a restaurant has food left
        self.assertTrue(self.r1.has_food())

        # Test to see if has_food returns True when a restaurant has 
        # just a little bit food left (i.e., food_left == 1)
		self.assertTrue(self.r5.has_food())
        
        # Test to see if has_food returns False when a restaurant has no food left
        self.assertFalse(self.r6.has_food())



    # Test order food
    def test_order_food(self):
        self.customer1 = Customer("Brenna", money = 0)
		self.rest1 = Restaurant("Fred's", food_left=0)
		self.driver1 = Driver("Sally", restaurants = [self.rest1])

		#testing the output when there is not enough money by showing that nothing has changed
		self.customer1.order_food(self.d2, self.r1)
		self.assertEqual(self.customer1.money, 0)
		self.assertEqual(self.d2.money, 500)
		self.assertEqual(self.r1.food_left, 10)

		#testing the output when there is no food by showing that nothing has changed
		self.c1.order_food(self.driver1, self.rest1)
		self.assertEqual(self.customer1.money, 50)
		self.assertEqual(self.driver1.money, 500)
		self.assertEqual(self.rest1.food_left, 0)
		
		#testing the output when the driver has no restaurant to go to by showing nothing has changed
		self.c1.order_food(self.d2, self.r3)
		self.assertEqual(self.c1.money, 50)
		self.assertEqual(self.d2.money, 500)
		self.assertEqual(self.r3.food_left, 10)

		#testing the output as orders go through by showing the change in money
		self.c1.order_food(self.d2, self.r1)
		self.assertEqual(self.c1.money, 30)

def main():
	rachel = Customer("Rachel", money = 300)
	izzy = Customer("Izzy", money = 200)
	charlies = Restaurant("Charlie's", money = 550, cost = 15, food_left = 12)
	skeeps = Restaurant("Skeeps", money = 400, cost = 20, food_left = 18)
	danny = Driver("Danny", money = 300, restaurants = [charlies, skeeps], delivery_fee = 10)
	george = Driver("George", money = 500, restaurants = [charlies], delivery_fee = 7)
	rachel.order_food(danny, skeeps)
	izzy.order_food(george, charlies)

if __name__ == "__main__":
    main()
    print("\n")
    unittest.main(verbosity = 2)   