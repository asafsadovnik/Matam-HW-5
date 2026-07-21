# TODO add all imports needed here

import json

class InvalidIdException(Exception): #def exceptions
    pass
class InvalidPriceException(Exception):
    pass


class Person:
    def __init__(self, person_id, name, city, address):

        if type(person_id) is not int or person_id < 0:
            raise InvalidIdException("Invalid Id provided")

        self.id = person_id
        self.name = name
        self.city = city
        self.address = address

    def __str__(self):
        class_name = type(self).__name__
        return f"{class_name}(id={self.id}, name='{self.name}', city='{self.city}', address='{self.address}')"



class Customer(Person):
    def __init__(self, person_id, name, city, address):
        super().__init__(person_id, name, city, address)
    """
    Represents a customer in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Customer name.
        - city (str): Customer city.
        - address (str): Customer shipping address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Customer(id=42, name='Daniel Elgarici', city='Karmiel, address='123 Main Street')
        Exact formatting requirements appear in the assignment PDF.
    """



class Supplier(Person):
    def __init__(self, person_id, name, city, address):
        super().__init__(person_id, name, city, address)
    """
    Represents a supplier in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Supplier name.
        - city (str): Warehouse city (origin city for shipping).
        - address (str): Warehouse address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Supplier(id=42, name='Yinon Goldshtein', city='Haifa, address='32 David Rose Street')
    """




class Product:
    def __init__(self, product_id, name, price, supplier_id, quantity):

        for val in (product_id, supplier_id, quantity):#check valid args
            if type(val) is not int or val < 0:
                raise InvalidIdException(f"Invalid {val} value provided")

        if type(price) not in (int, float) or price < 0:
            raise InvalidPriceException(f"Invalid price provided")

        self.id = product_id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.quantity = quantity

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, supplier_id={self.supplier_id}, quantity={self.quantity})"

    def __lt__(self, other):
        return self.price < other.price

    """
    Represents a product sold on the Matamazon website.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Product name.
        - price (float): Non-negative price.
        - supplier_id (int): ID of the supplier that provides the product.
        - quantity (int): Non-negative quantity in stock.

    Exceptions:
        InvalidIdException:
            - If id/supplier_id/quantity is invalid per specification.
        InvalidPriceException:
            - If price is invalid (e.g., negative).

    Printing:
        Must support printing in the following format (example):
            Product(id=101, name='Harry Potter Cushion', price=29.99, supplier_id=42, quantity=555)
    """




class Order:
    def __init__(self, order_id, customer_id, product_id, quantity, total_price):

        for val in (order_id, customer_id, product_id, quantity):#check valid args
            if type(val) is not int or val < 0:
                raise InvalidIdException(f"Invalid {val} value provided")

        if type(total_price) not in (int, float) or total_price < 0:
            raise InvalidPriceException(f"Invalid price provided")

        self.id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def __str__(self):
        return f"Order(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, quantity={self.quantity}, total_price={self.total_price})"


    """
    Represents a placed order.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier (assigned by the system).
        - customer_id (int): ID of the customer who placed the order.
        - product_id (int): ID of the ordered product.
        - quantity (int): Ordered quantity (non-negative integer).
        - total_price (float): Total price for the order (non-negative).

    Exceptions:
        InvalidIdException:
            - If one of the ID fields is invalid.
        InvalidPriceException:
            - If total_price is invalid.

    Printing:
        Must support printing in the following format (example):
            Order(id=1, customer_id=42, product_id=101, quantity=10, total_price=299.9)

    """




class MatamazonSystem:
    """
    Main system class that stores and manages customers, suppliers, products and orders.

    The system must support:
        - Registering customers/suppliers (with unique IDs across both types).
        - Adding/updating products (must validate supplier existence).
        - Placing orders (validate product existence and stock).
        - Removing objects by ID and type (with dependency constraints).
        - Searching products by name/query and optional max price.
        - Exporting system state to a text file (customers/suppliers/products only).
        - Exporting orders to JSON grouped by supplier origin city.

    Notes:
        - The specification does not require specific internal fields. Any data structures are allowed,
          as long as the behaviors match the spec.
        - A parameterless constructor is required.
    """

    def __init__(self):
        self.customer_dic = {}
        self.supplier_dic = {}
        self.product_dic = {}
        self.order_dic = {}

        self.next_order_id = 1 #tracker for available order id

        """
        Initialize an empty Matamazon system.

        Requirements:
            - Must be parameterless.
            - Internal collections may be chosen freely (dict/list, etc.).
        """



    def register_entity(self, entity, is_customer):

        if is_customer:
            if entity.id in self.customer_dic:
                raise InvalidIdException(f"Customer ID {entity.id} already exists")
            self.customer_dic[entity.id] = entity

        else:
            if entity.id in self.supplier_dic:
                raise InvalidIdException(f"Supplier ID {entity.id} already exists")
            self.supplier_dic[entity.id] = entity

        """
        Register a Customer or Supplier in the system.

        Args:
            entity: A Customer or Supplier object.
            is_customer (bool): True if entity is Customer, False if entity is Supplier.

        Raises:
            InvalidIdException:
                - If the entity ID is invalid.
                - If the entity ID already exists in the system (note: IDs must be unique across
                  customers AND suppliers).
        """


    def add_or_update_product(self, product):

        if product.supplier_id not in self.supplier_dic:
            raise InvalidIdException("Supplier not in the system")
        else:
            if product.id in self.product_dic:
                if product.supplier_id == self.product_dic[product.id].supplier_id:
                    self.product_dic[product.id] = product
                else:
                    raise InvalidIdException("Cannot update supplier for existing product")
            else:
                self.product_dic[product.id] = product

        """
        Add a new product or update an existing product.

        Behavior:
            - If product does not exist in system: add it.
            - If product exists:
                - It must belong to the same supplier as the existing one (same supplier_id),
                  otherwise raise InvalidIdException.
                - Update the stored product's fields according to the new product.

        Args:
            product: A Product object.

        Raises:
            InvalidIdException:
                - If the supplier_id does not exist in the system.
                - If attempting to update a product but supplier_id differs from the existing product.
        """


    def place_order(self, customer_id, product_id, quantity=1):

        if customer_id not in self.customer_dic: #check id
            raise InvalidIdException(f"Invalid customer Id provided {customer_id}")
        if product_id not in self.product_dic:
            return "The product does not exist in the system" #check if product exists and quantity good
        if quantity > self.product_dic[product_id].quantity:
            return "The quantity requested for this product is greater than the quantity in stock"
        else:
            total_price = self.product_dic[product_id].price * quantity #calc total price
            new_order = Order(self.next_order_id, customer_id, product_id, quantity, total_price) #create new order and increment id tracker
            self.order_dic[self.next_order_id] = new_order
            self.next_order_id += 1

            self.product_dic[product_id].quantity -= quantity #decrease quantity and return success
            return "The order has been accepted in the system"

        """
        Place an order for a product by a customer.

        Args:
            customer_id (int): Customer ID.
            product_id (int): Product ID.
            quantity (int, optional): Quantity to order. Defaults to 1.

        Returns:
            str: Status message according to specification:
                - "The order has been accepted in the system"
                - "The product does not exist in the system"
                - "The quantity requested for this product is greater than the quantity in stock"

        Behavior:
            - If product does not exist: return the relevant message.
            - If quantity requested > stock: return the relevant message.
            - Otherwise:
                - Decrease product stock by quantity.
                - Create a new Order with an auto-incremented system ID (starting at 1).
                - Store the order in the system.
                - Return success message.

        Notes:
            - The specification assumes quantity is an integer.
        """



    def remove_object(self, _id, class_type):

        if type(_id) is not int or _id < 0:
            raise InvalidIdException(f"Invalid Id provided {_id}")

        class_type = class_type.strip().capitalize() #clean string

        dics = { #check which case
            "Customer": self.customer_dic,
            "Supplier": self.supplier_dic,
            "Product": self.product_dic,
            "Order": self.order_dic
        }
        target_dic = dics[class_type]

        if _id not in target_dic:
            raise InvalidIdException(f"{class_type} Id not found {_id}")

        if class_type == "Order": #delete order and return quantity
            order_to_delete = self.order_dic[_id]
            self.product_dic[order_to_delete.product_id].quantity += order_to_delete.quantity #add quantity back to product
            del self.order_dic[_id]
            return order_to_delete.quantity

        for order in self.order_dic.values():
            if class_type == "Customer" and _id == order.customer_id:
                raise InvalidIdException(f"Cannot delete Customer with active order")
            elif class_type == "Product" and _id == order.product_id:
                raise InvalidIdException(f"Cannot delete Product with active order")
            elif class_type == "Supplier" and _id == self.product_dic[order.product_id].supplier_id:
                raise InvalidIdException(f"Cannot delete Supplier with an active order")

        del target_dic[_id]



        """
        Remove an object from the system by ID and type.

        Args:
            _id (int): Object ID to remove.
            class_type (str): One of: "Customer", "Supplier", "Product", "Order"
                              (exact casing/spelling per assignment).

        Returns:
            int | None:
                - If removing an Order: return the ordered quantity of that order (to restore stock).
                - Otherwise: no return value required.

        Raises:
            InvalidIdException:
                - If _id is not a valid non-negative integer.
                - If attempting to remove a Customer/Supplier/Product that still has dependent orders
                  in the system (i.e., orders that were not removed).
                - Additional InvalidIdException conditions as required by specification.
        """



    def search_products(self, query, max_price=None):

        if max_price is None: #check if max price limitation and set to max float size if none
            max_price = float('inf')

        search_results = [] #list for results

        for product in self.product_dic.values(): #check if substring + less then max price + has quantity
            if query in product.name and product.price <= max_price and product.quantity > 0:
                search_results.append(product)

        return sorted(search_results) #because of __lt__ method we can use sorted


        """
        Search products by query in the product name, and optionally filter by max_price.

        Args:
            query (str): Product name or part of product name.
            max_price (float, optional): If provided, only return products with price <= max_price.

        Returns:
            list[Product]:
                - Products that match the query and have quantity != 0,
                - Sorted by ascending price.
                - If no matching products exist, return an empty list.
        """



    def export_system_to_file(self, path):

        with open(path, 'w') as f: #open file stream in write mode and use print to file
            for cust in self.customer_dic.values():
                print(cust, file=f)
            for supp in self.supplier_dic.values():
                print(supp, file=f)
            for prod in self.product_dic.values():
                print(prod, file=f)

        """
        Export system state (customers, suppliers, products) to a text file.

        Args:
            path (str): Output file path.

        Behavior:
            - Write each object on its own line, using the object's print/str representation.
            - Orders must NOT be included.
            - No constraint on the ordering of objects in the output.

        Raises:
            OSError (or any file-open exception): Must be propagated to the caller.
        """



    def export_orders(self, out_file):

        city_orders = {} #create dictionary of cities - good for JSON format

        for order in self.order_dic.values():
            product = self.product_dic[order.product_id] #find city of product
            supplier = self.supplier_dic[product.supplier_id]
            city = supplier.city

            if city not in city_orders: #if city not in dic create new key
                city_orders[city] = []

            city_orders[city].append(str(order)) #add the order as a new string to the list of the city-orders. using str gets correct print format

        json.dump(city_orders, out_file) #automatic JSON format dump

        """
        Export orders in JSON format grouped by origin city.

        Args:
            out_file (file-like)

        Behavior (per specification):
            - Produce a JSON object where:
                - Keys: origin city (supplier city) for each order.
                - Values: list of strings representing orders (format as specified in section 4.1.4).
            - Order lists can be in any order.
            - No requirement on key ordering.

        Raises:
            Any exception during writing: Must be propagated to the caller.

        Notes:
            - The order origin city is the supplier city of the ordered product.
        """




def load_system_from_file(path):

    system = MatamazonSystem() #create empty system and list for prods
    product_list = []

    with open(path, 'r') as f:#open file to read
        for line in f:
            try:
                entity = eval(line) #use eval to instantly create object from our code

                if type(entity) == Customer:
                    system.register_entity(entity, True)
                elif type(entity) == Supplier:
                    system.register_entity(entity, False)
                elif type(entity) == Product: #if its product wait untill all customer and supplier are registered
                    product_list.append(entity)
            except (InvalidIdException, InvalidPriceException):
                raise #raise if its ID or Price error
            except Exception:
                pass #ignore all other errors

    for prod in product_list: #register prods
        system.add_or_update_product(prod)

    return system



    """
    Load a MatamazonSystem from an input file.

    Args:
        path (str): Path to a text file containing customers, suppliers and products.

    Returns:
        MatamazonSystem: Initialized system with the data found in the file.

    Behavior:
        - The file lines contain objects in the format produced by export_system_to_file (section 4.2).
        - Lines may appear in any order (e.g., product lines can appear before supplier lines).
        - Illegal lines may be ignored.
        - If an exception occurs during the creation of any required object due to invalid data,
          the function should stop and propagate the exception (as specified).

    Notes:
        - The assignment hints that eval() may be used.
    """



# TODO all the main part here