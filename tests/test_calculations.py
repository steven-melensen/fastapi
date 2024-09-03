import pytest
from app.calculations import add, subtract, multipy, divide, BankAccount, InsufficientFunds

#allows to not repeat bank_account = BackAccount() throughout the code
@pytest.fixture
def zero_bank_account():
    return BankAccount()

#allows to not repeat bank_account = BackAccount(50) 
@pytest.fixture
def bank_account():
    return BankAccount(50)


# The decorator allows to test many different sets of values
# You write a big string at first, the a list of tuples following the structure of your string
@pytest.mark.parametrize("num1, num2, expected",
    [
        (3, 2, 5),
        (7, 1, 8),
        (12, 4, 16)
    ]
)
def test_add(num1, num2, expected): #arguments should follow the naming convention of the decorator
    assert add(num1, num2) == expected
    
def test_subtract():
    assert subtract(9, 4) == 5
    
def test_multiply():
    assert multipy(5, 3) == 15
    
def test_divide():
    assert divide(6, 3) == 2
    
# initial version
'''
def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50
'''

# new version: no need to create the bank account instance
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20
    
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    # rounding because of float point precision
    assert round(bank_account.balance,5) == 55
    

@pytest.mark.parametrize("deposited, withdrew, expected",
    [
        (200, 100, 100),
        (50, 40, 10),
        (1200, 200, 1000)
    ])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected
    
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds): # deal with the error
        bank_account.withdraw(200) # More than what we have
        
        
        
        
