import unittest

class BankAccount:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("Wartość nie może być mniejsza od zera")
        
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Wpłacana kwota powinna być większa od zera")
        
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Wypłacana kwota powinna być większa od zera")
        
        if amount > self.balance:
            raise ValueError("Brak wystarczających środków do wypłaty")
        
        self.balance -= amount

    def get_balance(self):
        return self.balance
    
class TestBankAccount(unittest.TestCase):
    def test_initial_balance(self):
        account = BankAccount(100)
        self.assertEqual(account.get_balance(), 100)

        account = BankAccount()
        self.assertEqual(account.get_balance(), 0)

        with self.assertRaises(ValueError):
            BankAccount(-50) 

    def test_deposit(self):
        account = BankAccount(50)
        account.deposit(100)
        self.assertEqual(account.get_balance(), 150)

        with self.assertRaises(ValueError):
            account.deposit(0) 

        with self.assertRaises(ValueError):
            account.deposit(-10)

    def test_withdraw(self):
        account = BankAccount(200)
        account.withdraw(50)
        self.assertEqual(account.get_balance(), 150)

        with self.assertRaises(ValueError):
            account.withdraw(0)

        with self.assertRaises(ValueError):
            account.withdraw(-10)

        with self.assertRaises(ValueError):
            account.withdraw(500)

    def test_get_balance(self):
        account = BankAccount(300)
        self.assertEqual(account.get_balance(), 300)

if __name__ == "__main__":
    unittest.main()