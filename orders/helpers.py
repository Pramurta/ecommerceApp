def calculateTotalPrice(products):
    totalPrice = 0
    for product in products:
        totalPrice += product["price"]
    return totalPrice