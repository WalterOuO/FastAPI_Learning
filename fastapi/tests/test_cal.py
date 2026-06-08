from app.calculations import add, subtract, BankAccount, InsufficientFunds
import pytest


# pytest fixture 是一個用於在測試函數中提供固定數據或狀態的功能。它允許你在測試之前設置一些必要的條件，並在測試完成後進行清理。
@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount(starting_balance=0)

@pytest.fixture
def bank_account():
    return BankAccount(50)




@pytest.mark.parametrize("nums1, nums2, expected", [
    (5, 3, 8),
    (10, 2, 12),
    (-1, 1, 0)
])
def test_add(nums1, nums2, expected):
    print("Testing add function...")
    assert add(nums1, nums2) == expected


@pytest.mark.parametrize("nums1, nums2, expected", [
    (5, 3, 2),
    (10, 2, 8),
    (0, 1, -1)
])
def test_subtract(nums1, nums2, expected):
    print("Testing subtract function...")
    assert subtract(nums1, nums2) == expected


def test_bank_default_amount(zero_bank_account):
    print("Testing bank account with default amount...")
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
def test_bank_deposit():
    bank_account = BankAccount(starting_balance=100)
    bank_account.deposit(50)
    assert bank_account.balance == 150
    
    
def test_bank_withdraw():
    bank_account = BankAccount(starting_balance=100)
    bank_account.withdraw(30)
    assert bank_account.balance == 70

def test_bank_collect_interest():
    bank_account = BankAccount(starting_balance=100)
    bank_account.collect_interest(0.05)
    assert bank_account.balance == 105
    
    
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (100, 30, 70),
    (200, 50, 150),
    (50, 20, 30)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    # zero_bank_account.collect_interest(interest_rate)
    assert zero_bank_account.balance == expected
    


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(1000)