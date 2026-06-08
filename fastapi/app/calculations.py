def add(nums1: int, nums2: int) -> int:
    return nums1 + nums2

def subtract(nums1: int, nums2: int) -> int:
    return nums1 - nums2

def multiply(nums1: int, nums2: int) -> int:
    return nums1 * nums2

def divide(nums1: int, nums2: int) -> float:
    if nums2 == 0:
        raise ValueError("Cannot divide by zero")
    return nums1 / nums2


class InsufficientFunds(Exception):
    pass



class BankAccount:
    def __init__(self, starting_balance=0):
        # self.owner = owner
        self.balance = starting_balance

    def deposit(self, amount: float) -> None:
        # if amount <= 0:
        #     raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        # if amount <= 0:
        #     raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount
    
    def collect_interest(self, rate: float) -> None:
        # if rate < 0:
        #     raise ValueError("Interest rate cannot be negative")
        self.balance *= (1 + rate)
    
