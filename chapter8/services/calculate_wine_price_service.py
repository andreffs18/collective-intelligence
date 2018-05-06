class CalculateWinePriceService:

    def __init__(self, rating, age):
        self.rating = float(rating)
        self.age = float(age)

    def call(self):
        peak_age = self.rating - 50

        # Calculate price based on rating
        price = self.rating / 2
        if self.age > peak_age:
            # Past its peak, goes bad in 10 years
            price *= 5 - (self.age - peak_age) / 2
        else:
            # Increases to 5x original value as it
            # approaches its peak
            price *= 5 * ((self.age + 1) / peak_age)

        if price < 0:
            price = 0

        return price

