"""
Unit 0 Lab: Bank Account Simulator - Pytest Test Suite

This test file includes test cases for Bronze, Silver, and Gold tiers.
Run tests for specific tiers using pytest markers:
    pytest test_bank_lab.py -m bronze
    pytest test_bank_lab.py -m silver
    pytest test_bank_lab.py -m gold
    pytest test_bank_lab.py              # Run all tests

To run with verbose output:
    pytest test_bank_lab.py -v

Author: [Your Name]
Date: [Date]
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch
import importlib.util
import datetime


# ============================================================================
# TEST CONFIGURATION - Auto-detects student file in GitHub Classroom
# ============================================================================

import os
import glob

def find_student_file():
    """Auto-detect student Python file for GitHub Classroom."""
    # Look for files matching the expected pattern
    patterns = [
        "unit0_lab_*.py",      # Expected naming: unit0_lab_bronze.py, etc.
        "lab_sol.py",          # Solution file
        "*bank*.py",           # Any file with 'bank' in name
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern)
        # Exclude test files
        files = [f for f in files if not f.startswith('test_')]
        if files:
            return files[0]
    
    # If no match, look for any .py file that's not a test
    py_files = [f for f in glob.glob("*.py") if not f.startswith('test_')]
    if py_files:
        return py_files[0]
    
    raise FileNotFoundError("No student Python file found!")

# Try to auto-detect, fallback to default
try:
    STUDENT_FILE = find_student_file()
    print(f"Testing file: {STUDENT_FILE}")
except FileNotFoundError:
    STUDENT_FILE = "lab_sol.py"  # Default fallback


# ============================================================================
# HELPER FUNCTIONS TO LOAD STUDENT CODE
# ============================================================================

def load_student_module():
    """Dynamically load the student's Python file as a module."""
    spec = importlib.util.spec_from_file_location("student_module", STUDENT_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================================
# BRONZE TIER TESTS (70%)
# ============================================================================

@pytest.mark.bronze
class TestBronzeTier:
    """Tests for Bronze Tier requirements."""
    
    def test_is_valid_amount_exists(self):
        """Test that is_valid_amount function exists."""
        module = load_student_module()
        assert hasattr(module, 'is_valid_amount'), "is_valid_amount function not found"
    
    def test_is_valid_amount_positive(self):
        """Test is_valid_amount returns True for positive amounts."""
        module = load_student_module()
        assert module.is_valid_amount(10.0) == True
        assert module.is_valid_amount(0.01) == True
        assert module.is_valid_amount(100.50) == True
    
    def test_is_valid_amount_negative(self):
        """Test is_valid_amount returns False for negative amounts."""
        module = load_student_module()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = module.is_valid_amount(-10.0)
            assert result == False
            assert "Invalid" in fake_out.getvalue()
    
    def test_is_valid_amount_zero(self):
        """Test is_valid_amount returns False for zero."""
        module = load_student_module()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = module.is_valid_amount(0)
            assert result == False
            assert "Invalid" in fake_out.getvalue()
    
    def test_is_valid_amount_has_type_annotations(self):
        """Test that is_valid_amount has type annotations."""
        module = load_student_module()
        func = module.is_valid_amount
        annotations = func.__annotations__
        assert 'return' in annotations, "Missing return type annotation"
        assert annotations['return'] == bool, "Return type should be bool"
    
    def test_is_valid_amount_has_docstring(self):
        """Test that is_valid_amount has a docstring."""
        module = load_student_module()
        func = module.is_valid_amount
        assert func.__doc__ is not None, "Missing docstring"
        assert len(func.__doc__.strip()) > 10, "Docstring is too short"
    
    def test_deposit_functionality(self):
        """Test basic deposit functionality."""
        module = load_student_module()
        inputs = ['1', '50', '4']  # Deposit $50, then exit
        expected_outputs = ["Welcome", "50.00", "Deposit successful"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                for expected in expected_outputs:
                    assert expected in output, f"Expected '{expected}' not found in output"
    
    def test_withdrawal_functionality(self):
        """Test basic withdrawal functionality."""
        module = load_student_module()
        inputs = ['1', '100', '2', '30', '4']  # Deposit $100, withdraw $30, exit
        expected_outputs = ["Deposit successful", "Withdrawal successful"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                for expected in expected_outputs:
                    assert expected in output, f"Expected '{expected}' not found in output"
    
    def test_overdraft_limit_enforced(self):
        """Test that overdraft limit of -$100 is enforced."""
        module = load_student_module()
        inputs = ['1', '50', '2', '170', '4']  # Deposit $50, try to withdraw $170
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "denied" in output.lower() or "cannot exceed" in output.lower(), \
                    "Overdraft limit not enforced"
    
    def test_overdraft_limit_boundary(self):
        """Test that withdrawal up to -$100 is allowed."""
        module = load_student_module()
        inputs = ['1', '50', '2', '150', '4']  # Deposit $50, withdraw $150 (balance = -100)
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                # Should succeed since -100 is the limit
                assert "Withdrawal successful" in output or "successful" in output.lower()
    
    def test_invalid_deposit_amount(self):
        """Test that negative deposit amounts are rejected."""
        module = load_student_module()
        inputs = ['1', '-20', '50', '4']  # Try negative, then valid deposit
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "Invalid" in output, "Negative deposit should be rejected"


# ============================================================================
# SILVER TIER TESTS (85%)
# ============================================================================

@pytest.mark.silver
class TestSilverTier:
    """Tests for Silver Tier requirements (includes all Bronze tests)."""
    
    def test_view_summary_exists(self):
        """Test that view_summary function exists."""
        module = load_student_module()
        assert hasattr(module, 'view_summary'), "view_summary function not found"
    
    def test_view_summary_displays_correctly(self):
        """Test that view_summary displays balance and transaction count."""
        module = load_student_module()
        inputs = ['1', '50', '3', '4']  # Deposit, check balance, exit
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "50.00" in output, "Balance not displayed correctly"
                assert "1" in output or "Total Transactions: 1" in output, \
                    "Transaction count not displayed"
    
    def test_service_fee_applied_once(self):
        """Test that service fee is only applied once when going negative."""
        module = load_student_module()
        # Deposit $30, withdraw $50 (triggers fee), withdraw $10 (no fee)
        inputs = ['1', '30', '2', '50', '2', '10', '3', '4']
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Count how many times service fee message appears
                fee_count = output.lower().count("service fee")
                assert fee_count == 1, f"Service fee should appear once, found {fee_count} times"
    
    def test_service_fee_correct_amount(self):
        """Test that service fee is $2.00."""
        module = load_student_module()
        inputs = ['1', '30', '2', '50', '3', '4']  # Deposit $30, withdraw $50, check balance
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Balance should be: 30 - 50 - 2 = -22.00
                assert "-22.00" in output, "Service fee not calculated correctly"
    
    def test_no_service_fee_when_staying_positive(self):
        """Test that no service fee is charged when balance stays positive."""
        module = load_student_module()
        inputs = ['1', '100', '2', '30', '3', '4']  # Deposit $100, withdraw $30
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Should not contain service fee message
                assert "service fee" not in output.lower(), \
                    "Service fee should not be applied when balance stays positive"
    
    def test_invalid_menu_choice(self):
        """Test that invalid menu choices are handled."""
        module = load_student_module()
        inputs = ['9', '4']  # Invalid choice, then exit
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "Invalid" in output, "Invalid menu choice not handled"
    
    def test_two_decimal_places_formatting(self):
        """Test that all amounts are formatted to two decimal places."""
        module = load_student_module()
        inputs = ['1', '50.5', '3', '4']  # Deposit with one decimal
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "50.50" in output, "Amount should be formatted to two decimal places"
    
    def test_transaction_count_accuracy(self):
        """Test that transaction count is accurate."""
        module = load_student_module()
        # 3 transactions: deposit, withdraw, deposit
        inputs = ['1', '50', '2', '20', '1', '30', '3', '4']
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "3" in output or "Total Transactions: 3" in output, \
                    "Transaction count should be 3"


# ============================================================================
# GOLD TIER TESTS (100%)
# ============================================================================

@pytest.mark.gold
class TestGoldTier:
    """Tests for Gold Tier requirements (includes all Bronze and Silver tests)."""
    
    def test_datetime_imported(self):
        """Test that datetime module is imported."""
        module = load_student_module()
        assert hasattr(module, 'datetime'), "datetime module not imported"
    
    def test_view_history_exists(self):
        """Test that view_history function exists."""
        module = load_student_module()
        assert hasattr(module, 'view_history'), "view_history function not found"
    
    def test_transaction_history_option_exists(self):
        """Test that menu option 5 (View Transaction History) works."""
        module = load_student_module()
        inputs = ['1', '50', '5', '4']  # Deposit, view history, exit
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                assert "Transaction History" in output or "DEPOSIT" in output, \
                    "Transaction history not displayed"
    
    def test_transaction_history_format(self):
        """Test that transaction history has correct format with timestamps."""
        module = load_student_module()
        inputs = ['1', '50', '5', '4']  # Deposit, view history, exit
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Check for timestamp format [YYYY-MM-DD HH:MM:SS]
                assert "[" in output and "]" in output, "Timestamp brackets not found"
                assert "DEPOSIT" in output or "WITHDRAWAL" in output, \
                    "Transaction type not recorded"
                assert "$" in output, "Amount not recorded in history"
    
    def test_transaction_history_records_deposits(self):
        """Test that deposits are recorded in transaction history."""
        module = load_student_module()
        inputs = ['1', '50', '1', '30', '5', '4']  # Two deposits, view history
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Should show both deposits
                deposit_count = output.count("DEPOSIT")
                assert deposit_count >= 2, f"Expected 2 deposits, found {deposit_count}"
    
    def test_transaction_history_records_withdrawals(self):
        """Test that withdrawals are recorded in transaction history."""
        module = load_student_module()
        inputs = ['1', '100', '2', '30', '5', '4']  # Deposit, withdraw, view history
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                assert "WITHDRAWAL" in output, "Withdrawal not recorded in history"
    
    def test_transaction_history_order(self):
        """Test that transaction history maintains chronological order."""
        module = load_student_module()
        inputs = ['1', '50', '2', '20', '1', '30', '5', '4']
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Find positions of transaction types
                first_deposit = output.find("DEPOSIT")
                withdrawal = output.find("WITHDRAWAL")
                second_deposit = output.rfind("DEPOSIT")
                
                # Check order: deposit, withdrawal, deposit
                assert first_deposit < withdrawal < second_deposit, \
                    "Transaction history not in chronological order"
    
    def test_transaction_history_amounts_formatted(self):
        """Test that amounts in history are formatted to two decimal places."""
        module = load_student_module()
        inputs = ['1', '50.5', '5', '4']  # Deposit with one decimal
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Check for $50.50 format in history
                assert "$50.50" in output, "Transaction history amounts not formatted correctly"


# ============================================================================
# INTEGRATION TESTS (All Tiers)
# ============================================================================

@pytest.mark.integration
class TestIntegration:
    """Integration tests that cover multiple features across tiers."""
    
    def test_complete_banking_session(self):
        """Test a complete banking session with multiple operations."""
        module = load_student_module()
        inputs = [
            '1', '100',      # Deposit $100
            '2', '30',       # Withdraw $30
            '3',             # Check balance
            '1', '50',       # Deposit $50
            '2', '150',      # Withdraw $150 (triggers service fee)
            '5',             # View history
            '4'              # Exit
        ]
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Verify various aspects
                assert "Welcome" in output
                assert "Deposit successful" in output
                assert "Withdrawal successful" in output
                assert "Service fee" in output
                assert "Transaction History" in output or "DEPOSIT" in output
                assert "Thank you" in output
    
    def test_rejected_withdrawal_not_in_history(self):
        """Test that rejected withdrawals are not recorded in history."""
        module = load_student_module()
        inputs = ['1', '50', '2', '170', '5', '4']  # Deposit, rejected withdrawal, history
        
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    module.main()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                
                # Should only have 1 DEPOSIT, no WITHDRAWAL
                assert output.count("DEPOSIT") >= 1
                assert "denied" in output.lower() or "cannot exceed" in output.lower()
                # Withdrawal should not be in history since it was rejected
                withdrawal_in_history = output[output.find("Transaction History"):].count("WITHDRAWAL")
                assert withdrawal_in_history == 0, "Rejected withdrawal should not be in history"


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure custom markers to avoid warnings."""
    config.addinivalue_line("markers", "bronze: Bronze tier tests (70%)")
    config.addinivalue_line("markers", "silver: Silver tier tests (85%)")
    config.addinivalue_line("markers", "gold: Gold tier tests (100%)")
    config.addinivalue_line("markers", "integration: Integration tests")


# ============================================================================
# Run this file with: pytest test_bank_lab.py -v
# Or run specific tiers: pytest test_bank_lab.py -m bronze -v
# ============================================================================


if __name__ == "__main__":
    print("Run tests using: pytest test_bank_lab.py")
    print("For specific tiers: pytest test_bank_lab.py -m bronze")