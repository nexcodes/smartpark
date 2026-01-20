"""
Main test runner for SmartPark System
Discovers and runs all test modules in the tests folder
"""

import sys
import os
import unittest

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


def run_all_tests():
    """
    Discover and run all test modules
    """
    # Get the directory containing this script
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover all test files
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)
    
    # Return exit code (0 for success, 1 for failure)
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_module):
    """
    Run a specific test module
    
    Args:
        test_module (str): Name of the test module (without .py extension)
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def list_available_tests():
    """
    List all available test modules
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f[:-3] for f in os.listdir(test_dir) 
                  if f.startswith('test_') and f.endswith('.py')]
    
    print("\nAvailable test modules:")
    print("="*70)
    for i, test_file in enumerate(test_files, 1):
        print(f"{i}. {test_file}")
    print("="*70)


def get_available_tests():
    """
    Get list of available test modules
    
    Returns:
        list: List of test module names
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f[:-3] for f in os.listdir(test_dir) 
                  if f.startswith('test_') and f.endswith('.py') and f != 'test.py']
    return sorted(test_files)


def display_menu():
    """
    Display interactive test menu
    """
    test_modules = get_available_tests()
    
    print("\n" + "="*70)
    print("SMARTPARK TEST RUNNER - INTERACTIVE MODE")
    print("="*70)
    print("\n📋 Available Test Modules:")
    print("-"*70)
    
    for i, module in enumerate(test_modules, 1):
        print(f"  {i}. {module}")
    
    print(f"  {len(test_modules) + 1}. Run ALL tests")
    print(f"  0. Exit")
    print("-"*70)


def interactive_mode():
    """
    Run tests in interactive mode
    """
    while True:
        test_modules = get_available_tests()
        display_menu()
        
        try:
            choice = input("\n👉 Enter your choice: ").strip()
            
            if choice == '0':
                print("\n✅ Exiting test runner. Goodbye!\n")
                break
            
            choice_num = int(choice)
            
            if choice_num == len(test_modules) + 1:
                # Run all tests
                print(f"\n{'='*70}")
                print("🚀 Running ALL SmartPark tests")
                print(f"{'='*70}\n")
                exit_code = run_all_tests()
                
                if exit_code == 0:
                    print("\n✅ All tests passed!")
                else:
                    print("\n❌ Some tests failed!")
                
            elif 1 <= choice_num <= len(test_modules):
                # Run specific test
                selected_module = test_modules[choice_num - 1]
                print(f"\n{'='*70}")
                print(f"🚀 Running test module: {selected_module}")
                print(f"{'='*70}\n")
                exit_code = run_specific_test(selected_module)
                
                if exit_code == 0:
                    print(f"\n✅ {selected_module} passed!")
                else:
                    print(f"\n❌ {selected_module} failed!")
            else:
                print("\n❌ Invalid choice! Please select a valid option.")
                
        except ValueError:
            print("\n❌ Invalid input! Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n✅ Exiting test runner. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Ask if user wants to continue
        if choice != '0':
            continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
            if continue_choice == 'q':
                print("\n✅ Exiting test runner. Goodbye!\n")
                break


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SmartPark Test Runner')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List all available test modules')
    parser.add_argument('-m', '--module', type=str,
                       help='Run a specific test module (e.g., test_parking_system)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode (default if no args)')
    
    args = parser.parse_args()
    
    # If no arguments provided, run in interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
        sys.exit(0)
    
    if args.list:
        list_available_tests()
        sys.exit(0)
    
    if args.interactive:
        interactive_mode()
        sys.exit(0)
    
    if args.module:
        print(f"\n{'='*70}")
        print(f"Running test module: {args.module}")
        print(f"{'='*70}\n")
        exit_code = run_specific_test(args.module)
    else:
        print(f"\n{'='*70}")
        print("Running all SmartPark tests")
        print(f"{'='*70}\n")
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
