# Unit 0 Lab: Bank Account Simulator

**Task**: You are building a bank account simulator for Goetz where students can deposit money, withdraw money, check their balance, and exit.
The lab is divided into three tiers. 

Each tier builds directly on the previous one. Do not start a new file, just keep adding to your existing one.

**File naming**: use this format to indicate the tier you attempted: `unit0_lab_tier.py`, ex. unit0_lab_gold.py

**Submission**: Push your completed file to your GitHub repository. Make sure your file is in the correct folder before submitting.

---

## Table of Contents
- [Bronze Tier (Max Grade: 70%)](#bronze-tier-max-grade-70)
- [Silver Tier (Max Grade: 85%)](#silver-tier-max-grade-85)
- [Gold Tier (Max Grade: 100%)](#gold-tier-max-grade-100)
- [Notes](#notes)
- [Starter Code](#starter-code)

---

## Bronze Tier (Max Grade: 70%)
**Goal**: Get the core program working.

Write a menu-driven program in the `main()` function that loops until the user exits using sentinel value:
1. Deposit money
2. Withdraw money
3. Check balance
4. Exit

**Requirements**:
- Use a `float` variable to store the account balance (start at $0.00)
- Use an `int` to track the menu choices
- Validate that deposit and withdrawal amounts are positive numbers by writing the function `is_valid_amount()`. Include a docstring and type annotations
- Prevent balance from going below -$100.00 (overdraft limit) in `main()` function

### Bronze Success Criteria
- Menu repeats until user exits
- Deposits and withdrawals update balance correctly
- Negative and zero amounts are rejected
- Overdraft limit of -$100.00 is enforced
- `is_valid_amount()` has a docstring and type annotations

### Bronze Sample Output
```
Welcome to the Goetz Bank!

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 1
Enter deposit amount: -20
Invalid amount. Please enter a positive number.
Enter deposit amount: 50
Deposit successful! You deposited $50.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 2
Enter withdrawal amount: 170
Withdrawal denied! You cannot exceed the overdraft limit of -$100.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 2
Enter withdrawal amount: 80
Withdrawal successful! You withdrew $80.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 3
Current balance: $-30.00

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 4
Thank you for banking with us!
```

---

## Silver Tier (Max Grade: 85%)
**Goal**: Add a service fee and improve input handling.

**Keep all Bronze code**, then add:
- Update 3rd menu option - **Check Balance**: shows current balance and total number of transactions (deposits + withdrawals) by implementing the function `view_summary()` and calling it in `main()`. You might need a counter to track the number of deposits/withdrawals made.
- Apply a $2.00 service fee when the balance goes below $0.00 (only charged once when balance becomes negative)
- Format all dollar amounts to two decimal places
- Handle invalid menu input (e.g. `"9"`). You may assume the test case will try using numbers as invalid inputs.

### Silver Success Criteria
- All Bronze criteria met
- Service fee is applied correctly (only once when balance becomes negative)
- Account summary displays balance and transaction count
- Invalid menu choices show an appropriate error message

### Silver Sample Run
```
Welcome to the Goetz Bank!

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 9
Invalid choice. Please enter a number between 1 and 4.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 1
Enter deposit amount: 30
Deposit successful! You deposited $30.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 2
Enter withdrawal amount: 50
Withdrawal successful! You withdrew $50.00.
Service fee of $2.00 applied for overdraft.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
Enter your choice: 3
Account Summary:
Current Balance: $-22.00
Total Transactions: 2

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 4
Thank you for banking with us!
```

---

## Gold Tier (Max Grade: 100%)
**Goal**: Add a timestamped transaction history.

**Keep all Silver code**, then add:
- Add a 5th menu option: **View Transaction History**
- Every time a deposit or withdrawal is made, record the action, amount, and timestamp by adding it into a `list` (Hint: use `datetime` module)
- Viewing transaction history function takes a `list` and prints each entry in the format: `[YYYY-MM-DD HH:MM:SS] DEPOSIT/WITHDRAWAL: $Amount`. Hint: use .strftime("%Y-%m-%d %H:%M:%S") to make the time stamp in this format.

### Gold Success Criteria
- All Silver criteria met
- Every deposit/withdrawal is timestamped and stored
- Transaction history displays clearly and in order

### Gold Sample Run
```
Welcome to the Goetz Bank!

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 1
Enter deposit amount: 100
Deposit successful! You deposited $100.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 2
Enter withdrawal amount: 40
Withdrawal successful! You withdrew $40.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 1
Enter deposit amount: 25
Deposit successful! You deposited $25.00.

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 5
Transaction History:
[2025-09-08 10:15:22] DEPOSIT: $100.00
[2025-09-08 10:15:35] WITHDRAWAL: $40.00
[2025-09-08 10:15:48] DEPOSIT: $25.00

Bank Menu:
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Exit
5. View Account Summary
Enter your choice: 4
Thank you for banking with us!
```

---

## Notes
1. Include a **header comment** at the top of your file (name, date, course, description)
2. Add comments throughout your program to explain complex code, IPO comments should be in the main function.
3. Breathe :)

---

## Starter Code

```python
# ADD HEADER COMMENT

# TODO (Gold): import datetime here


# BRONZE FUNCTIONS

def is_valid_amount(amount): # TODO: add Type Annotations
    """
    # TODO: write the docstring
    """
    # TODO: implement this function
    pass


def display_menu() -> None:
    """
    Prints the bank menu options to the screen.
    """
    print("\nBank Menu:")
    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. Check Balance")
    print("4. Exit")
    # TODO (Gold): add option 5 - View Transaction History


# SILVER FUNCTION

def view_summary(balance: float, transaction_count: int) -> None:
    """
    Displays the account summary with balance and transaction count.

    Args:
        balance (float): The current account balance.
        transaction_count (int): The total number of transactions made.
    """
    # TODO (Silver): implement this function
    pass


# GOLD FUNCTION

def view_history(transaction_history: list) -> None:
    """
    Displays all transaction history entries with timestamps.

    Args:
        transaction_history (list): The list of transaction entries to display.
    """
    # TODO (Gold): implement this function
    pass


# ===================== MAIN =====================

def main() -> None:
    """
    Main function that runs the bank account simulator.
    """
    # TODO: initialize variables needed for this system
    # balance (float), transaction_count (int), service_fee_charged (bool for Silver)

    print("Welcome to the Goetz Bank!")

    # TODO: loop until the user exits
    #   display the menu, get input, and handle each option:
    #   1 - Ask for deposit amount, validate, add to balance (For Gold, append the timestamp)
    #   2 - Ask for withdrawal amount, validate, check overdraft limit, subtract from balance (For Silver, check if service fee applies) (For Gold, append the timestamp)
    #   3 - Display current balance
    #   4 - Exit with goodbye message
    #   5 (Silver) - Call view_summary()
    #   6 (Gold) - Call view_history()
    #   Message for any invalid options    

if __name__ == '__main__':
    main()
```
