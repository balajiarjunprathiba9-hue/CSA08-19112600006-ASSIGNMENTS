
from decimal import Decimal, ROUND_HALF_UP


def get_base_rate(season, old_base_rate):
    if season.lower() in ["april", "may", "june"]:
        return Decimal("32.00")

    return Decimal(str(old_base_rate))


def calculate_bonus(quantity):
    if quantity > 500:
        return Decimal("0.50") * quantity

    return Decimal("0.00")


def calculate_payment(fat, snf, quantity, season, old_base_rate):
    base_rate = get_base_rate(season, old_base_rate)

    # Calculate rate using the fat reading
    milk_rate = base_rate + fat * Decimal("0.45")

    bonus = calculate_bonus(quantity)

    total = milk_rate * quantity + bonus

    total = total.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return milk_rate, bonus, total


# Get user inputs
season = input("Enter month: ").lower()
old_rate = input("Enter original base rate for other months: ")

fat = Decimal(input("Enter fat reading: "))
snf = Decimal(input("Enter SNF reading: "))
quantity = Decimal(input("Enter quantity in litres: "))


# Calculate payment
rate, bonus, total = calculate_payment(
    fat, snf, quantity, season, old_rate
)


# Display results
print("\n--- Milk Payment Details ---")
print("Fat:", format(fat, ".2f"))
print("SNF:", format(snf, ".2f"))
print("Rate per litre: Rs.", rate.quantize(Decimal("0.01")))
print("Bonus: Rs.", bonus.quantize(Decimal("0.01")))
print("Total payment: Rs.", total)
