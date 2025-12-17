"""
ENGI9818 – Fall 2025 | Make-Up Task
Bank Account System Implementation

Author: Fatema Tuj Johora

This module implements a `BankAccount` class that demonstrates Python OOP
concepts, including properties, class/staticmethods, a custom exception
hierarchy, robust validation, and transaction history management.
"""

from __future__ import annotations
from typing import List, Tuple, Union


# ---------- Custom Exception Hierarchy ----------

class BankAccountError(Exception):
    """Base exception for bank account errors."""
    pass


class InsufficientFundsError(BankAccountError):
    """Raised when withdrawal amount exceeds balance."""

    def __init__(self, balance: float, amount: float) -> None:
        message = (
            f"Insufficient funds: balance = {balance:.2f}, "
            f"attempted = {amount:.2f}"
        )
        super().__init__(message)


class InvalidAmountError(BankAccountError):
    """Raised when amount is invalid (negative or zero)."""

    def __init__(self, amount: object) -> None:
        super().__init__(
            f"Invalid amount: {amount!r}. Must be a positive number."
        )


class InvalidAccountError(BankAccountError):
    """Raised when account operation is invalid."""

    def __init__(self, message: str = "Invalid account operation.") -> None:
        super().__init__(message)


# ---------- BankAccount Class Implementation ----------

class BankAccount:
    """
    Represents a bank account with deposit, withdrawal, and transfer
    operations. The class showcases:

    - Encapsulation via property getters/setters.
    - Alternative constructors (`from_balance`, `from_string`).
    - Validation with a static method (`_validate_amount`).
    - Custom exceptions for precise error handling.
    - Transaction history retention.
    """

    _account_counter: int = 1000  # auto-incrementing account number

    def __init__(
        self,
        account_holder: str,
        initial_balance: Union[int, float] = 0,
        status: str = "active",
    ) -> None:
        """
        Initialize a new bank account.

        Parameters
        ----------
        account_holder : str
            The account holder's full name.
        initial_balance : int | float, optional
            Starting balance (must be >= 0), by default 0.
        status : str, optional
            Account status: either "active" or "inactive", by default "active".

        Raises
        ------
        InvalidAmountError
            If `initial_balance` is not numeric or is negative.
        InvalidAccountError
            If `status` is not one of {"active", "inactive"}.
        """
        # Allow zero at construction time (>= 0),
        # while operations require > 0 via _validate_amount.
        if not isinstance(initial_balance, (int, float)):
            raise InvalidAmountError(initial_balance)
        if initial_balance < 0:
            raise InvalidAmountError(
                f"Balance cannot be negative: {initial_balance!r}"
            )
        if status not in ("active", "inactive"):
            raise InvalidAccountError(
                "Status must be 'active' or 'inactive'."
            )

        BankAccount._account_counter += 1
        self._account_number: int = BankAccount._account_counter
        self._account_holder: str = account_holder
        self._balance: float = float(initial_balance)
        self._status: str = status
        # (action, amount, resulting_balance[, other_account_number])
        self._transactions: List[Tuple] = []

        # Record account creation
        self._transactions.append(
            ("Account created", self._balance, self._balance)
        )

    # ---------- Representation ----------

    def __repr__(self) -> str:
        """Return an unambiguous representation for debugging."""
        return (
            f"BankAccount(holder={self._account_holder!r}, "
            f"number={self._account_number}, balance={self._balance:.2f}, "
            f"status={self._status!r})"
        )

    # ---------- Property Decorators ----------

    @property
    def balance(self) -> float:
        """float: Current account balance."""
        return self._balance

    @balance.setter
    def balance(self, new_value: Union[int, float]) -> None:
        """
        Set the account balance with validation.

        Parameters
        ----------
        new_value : int | float
            The new balance value. Must be numeric and >= 0.

        Raises
        ------
        InvalidAmountError
            If the value is not numeric or is negative.
        """
        if not isinstance(new_value, (int, float)):
            raise InvalidAmountError(new_value)
        if new_value < 0:
            raise InvalidAmountError(
                f"Balance cannot be negative: {new_value!r}"
            )
        self._balance = float(new_value)

    @property
    def account_holder(self) -> str:
        """str: The account holder's name."""
        return self._account_holder

    @property
    def account_number(self) -> int:
        """int: The unique account number."""
        return self._account_number

    @property
    def status(self) -> str:
        """str: The current account status: 'active' or 'inactive'."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the account status.

        Parameters
        ----------
        value : str
            Either "active" or "inactive".

        Raises
        ------
        InvalidAccountError
            If the value is not one of {"active", "inactive"}.
        """
        if value not in ("active", "inactive"):
            raise InvalidAccountError(
                "Status must be 'active' or 'inactive'."
            )
        self._status = value

    # ---------- Class Method Decorators ----------

    @classmethod
    def from_balance(
        cls, account_holder: str, initial_balance: Union[int, float]
    ) -> "BankAccount":
        """
        Create a new `BankAccount` using an explicit starting balance.

        Returns
        -------
        BankAccount
            A new account instance.
        """
        return cls(account_holder, initial_balance)

    @classmethod
    def from_string(cls, account_data: str) -> "BankAccount":
        """
        Parse a semicolon-delimited string and create a `BankAccount`.

        The expected format is:
        `"account_holder;balance;status"`.

        Parameters
        ----------
        account_data : str
            The string to parse.

        Returns
        -------
        BankAccount
            A new account constructed from the parsed values.

        Raises
        ------
        InvalidAccountError
            If the string cannot be parsed or contains invalid values.
        """
        try:
            name, balance_text, status_text = account_data.split(";")
            return cls(name.strip(), float(balance_text), status_text.strip())
        except Exception as exc:  # noqa: BLE001 (keep broad for clear message)
            raise InvalidAccountError(
                f"Failed to parse account string: {exc}"
            ) from exc

    # ---------- Static Method Decorator ----------

    @staticmethod
    def _validate_amount(amount: Union[int, float]) -> bool:
        """
        Validate that an amount is numeric and strictly positive (> 0).

        Parameters
        ----------
        amount : int | float
            The amount to validate.

        Returns
        -------
        bool
            True if valid.

        Raises
        ------
        InvalidAmountError
            If the amount is not numeric or not strictly positive.
        """
        if not isinstance(amount, (int, float)):
            raise InvalidAmountError(amount)
        if amount <= 0:
            raise InvalidAmountError(amount)
        return True

    # ---------- Core Banking Operations ----------

    def _ensure_active(self) -> None:
        """Ensure that the account is active before a transaction."""
        if self._status != "active":
            raise InvalidAccountError(
                f"Account {self._account_number} is not active for "
                "transactions."
            )

    def deposit(self, amount: Union[int, float]) -> float:
        """
        Deposit funds into the account.

        Parameters
        ----------
        amount : int | float
            The amount to deposit (must be > 0).

        Returns
        -------
        float
            The new balance after deposit.

        Raises
        ------
        InvalidAccountError
            If the account is not active.
        InvalidAmountError
            If `amount` is not strictly positive.
        """
        self._ensure_active()
        self._validate_amount(amount)
        self._balance += amount
        self._transactions.append(("Deposit", amount, self._balance))
        return self._balance

    def withdraw(self, amount: Union[int, float]) -> float:
        """
        Withdraw funds from the account if sufficient balance exists.

        Parameters
        ----------
        amount : int | float
            The amount to withdraw (must be > 0).

        Returns
        -------
        float
            The new balance after withdrawal.

        Raises
        ------
        InvalidAccountError
            If the account is not active.
        InvalidAmountError
            If `amount` is not strictly positive.
        InsufficientFundsError
            If `amount` exceeds the available balance.
        """
        self._ensure_active()
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        self._transactions.append(("Withdraw", amount, self._balance))
        return self._balance

    def transfer(self, amount: Union[int, float], target_account: "BankAccount"
                 ) -> bool:
        """
        Transfer funds to another `BankAccount`.

        Parameters
        ----------
        amount : int | float
            The amount to transfer (must be > 0).
        target_account : BankAccount
            The destination account.

        Returns
        -------
        bool
            True if the transfer completes successfully.

        Raises
        ------
        InvalidAccountError
            If this account is not active or target is not a BankAccount.
        InvalidAmountError
            If `amount` is not strictly positive.
        InsufficientFundsError
            If `amount` exceeds the available balance.
        """
        self._ensure_active()
        if not isinstance(target_account, BankAccount):
            raise InvalidAccountError(
                "Target must be a BankAccount instance."
            )
        self._validate_amount(amount)

        # Perform transfer using validated operations
        self.withdraw(amount)
        target_account.deposit(amount)
        self._transactions.append(
            ("Transfer to", amount, self._balance,
             target_account.account_number)
        )
        target_account._transactions.append(
            ("Transfer from", amount, target_account._balance,
             self.account_number)
        )
        return True

    def get_transaction_history(self) -> List[Tuple]:
        """
        Return a copy of the transaction history.

        Returns
        -------
        list[tuple]
            A list of transaction tuples in chronological order.
        """
        return list(self._transactions)


# ---------- Basic Testing Examples (matches handout) ----------
if __name__ == "__main__":
    # Create accounts using different constructors
    account1 = BankAccount("John Doe", 1000)
    account2 = BankAccount.from_balance("Jane Smith", 500)
    account3 = BankAccount.from_string("Bob Wilson;750;active")

    # Test basic operations
    account1.deposit(200)
    account1.withdraw(100)
    account1.transfer(300, account2)

    # Show results with requested labels
    print("Account 1 balance:", account1.balance)
    print("Account 1 history:", account1.get_transaction_history())
    print("Account 2 balance:", account2.balance)
    print("Account 2 history:", account2.get_transaction_history())

    # Test error conditions
    try:
        account1.withdraw(2000)  # Should raise InsufficientFundsError
    except InsufficientFundsError as exc:
        print(f"Expected error: {exc}")

    try:
        account1.deposit(-50)  # Should raise InvalidAmountError
    except InvalidAmountError as exc:
        print(f"Expected error: {exc}")


