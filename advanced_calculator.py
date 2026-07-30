import math
import json
import os
import numpy as np
from datetime import datetime

class CalculatorHistory:
    """Manages saving and loading calculation history using JSON."""
    def __init__(self, filename="calc_history.json"):
        self.filename = filename

    def save_record(self, expression, result):
        history = self.load_records()
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expression": expression,
            "result": result
        }
        history.append(record)
        with open(self.filename, 'w') as f:
            json.dump(history, f, indent=4)

    def load_records(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def display_history(self):
        records = self.load_records()
        if not records:
            print("\n[INFO] No history found.")
            return
        print("\n--- Calculation History ---")
        for idx, rec in enumerate(records[-10:], 1):  # Show last 10 records
            print(f"{idx}. [{rec['timestamp অ্যাক']}]: {rec['expression']} = {rec['result']}")
        print("-" * 28)


class AdvancedCalculator:
    """Core calculator engine supporting scientific, matrix, and unit conversion operations."""
    
    def __init__(self):
        self.history = CalculatorHistory()

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero is mathematically undefined.")
        return a / b

    def power(self, base, exp): return math.pow(base, exp)
    def square_root(self, x):
        if x < 0:
            raise ValueError("Cannot calculate square root of a negative number in real domain.")
        return math.sqrt(x)

    def logarithm(self, x, base=math.e):
        if x <= 0:
            raise ValueError("Logarithm domain error: input must be greater than zero.")
        return math.log(x, base)

    # Trigonometric functions (input in degrees converted to radians)
    def sin(self, angle_deg): return math.sin(math.radians(angle_deg))
    def cos(self, angle_deg): return math.cos(math.radians(angle_deg))
    def tan(self, angle_deg): return math.tan(math.radians(angle_deg))

    # Matrix Operations using NumPy
    def matrix_operation(self):
        print("\n--- Matrix Operations ---")
        print("1. Addition\n2. Multiplication\n3. Determinant")
        choice = input("Select matrix operation (1-3): ").strip()

        try:
            if choice in ['1', '2']:
                print("Enter Matrix A (row-wise, space-separated values, rows separated by semicolon):")
                # Example: 1 2; 3 4
                mat_a_str = input("Matrix A: ")
                mat_a = np.matrix(mat_a_str)

                print("Enter Matrix B:")
                mat_b_str = input("Matrix B: ")
                mat_b = np.matrix(mat_b_str)

                if choice == '1':
                    result = mat_a + mat_b
                else:
                    result = np.dot(mat_a, mat_b)
                
                print("\nResult Matrix:\n", result)
                self.history.save_record(f"Matrix Op {choice}", str(result.tolist()))

            elif choice == '3':
                mat_str = input("Enter Matrix (e.g., 1 2; 3 4): ")
                mat = np.array(np.matrix(mat_str))
                result = np.linalg.det(mat)
                print(f"\nDeterminant: {result}")
                self.history.save_record(f"Matrix Determinant", result)
            else:
                print("[ERROR] Invalid selection.")
        except Exception as e:
            print(f"[MATRIX ERROR] {e}")

    # Unit Conversions
    def unit_converter(self):
        print("\n--- Unit Converter ---")
        print("1. Celsius to Fahrenheit\n2. Kilometers to Miles\n3. Kilograms to Pounds")
        choice = input("Choose conversion type (1-3): ").strip()

        try:
            val = float(input("Enter value to convert: "))
            if choice == '1':
                res = (val * 9/5) + 32
                expr = f"{val}°C to °F"
            elif choice == '2':
                res = val * 0.621371
                expr = f"{val} km to miles"
            elif choice == '3':
                res = val * 2.20462
                expr = f"{val} kg to lbs"
            else:
                print("[ERROR] Invalid choice.")
                return
            
            print(f"Result: {res}")
            self.history.save_record(expr, res)
        except ValueError:
            print("[ERROR] Please enter a valid numerical value.")


def main():
    calc = AdvancedCalculator()

    while True:
        print("\n==============================")
        print("   ADVANCED PYTHON CALCULATOR ")
        print("==============================")
        print("1. Basic Arithmetic (+, -, *, /)")
        print("2. Scientific Calculations (Power, Root, Log, Trig)")
        print("3. Matrix Operations")
        print("4. Unit Converter")
        print("5. View Calculation History")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            try:
                a = float(input("Enter first number: "))
                op = input("Enter operator (+, -, *, /): ").strip()
                b = float(input("Enter second number: "))

                if op == '+': res = calc.add(a, b)
                elif op == '-': res = calc.subtract(a, b)
                elif op == '*': res = calc.multiply(a, b)
                elif op == '/': res = calc.divide(a, b)
                else:
                    print("[ERROR] Invalid operator.")
                    continue

                print(f"Result: {a} {op} {b} = {res}")
                calc.history.save_record(f"{a} {op} {b}", res)
            except Exception as e:
                print(f"[ERROR] {e}")

        elif choice == '2':
            print("\n--- Scientific Mode ---")
            print("1. Power (x^y)\n2. Square Root\n3. Logarithm\n4. Sin, Cos, Tan")
            sci_choice = input("Select function (1-4): ").strip()

            try:
                if sci_choice == '1':
                    base = float(input("Base: "))
                    exp = float(input("Exponent: "))
                    res = calc.power(base, exp)
                    expr = f"{base}^{exp}"
                elif sci_choice == '2':
                    num = float(input("Number: "))
                    res = calc.square_root(num)
                    expr = f"sqrt({num})"
                elif sci_choice == '3':
                    num = float(input("Number: "))
                    base = float(input("Base (default is e, enter 0 for natural log): "))
                    base = math.e if base == 0 else base
                    res = calc.logarithm(num, base)
                    expr = f"log_{base}({num})"
                elif sci_choice == '4':
                    trig_func = input("Function (sin/cos/tan): ").strip().lower()
                    angle = float(input("Angle in degrees: "))
                    if trig_func == 'sin': res = calc.sin(angle)
                    elif trig_func == 'cos': res = calc.cos(angle)
                    elif trig_func == 'tan': res = calc.tan(angle)
                    else:
                        print("[ERROR] Invalid trig function.")
                        continue
                    expr = f"{trig_func}({angle}°)"
                else:
                    print("[ERROR] Invalid choice.")
                    continue

                print(f"Result: {res}")
                calc.history.save_record(expr, res)
            except Exception as e:
                print(f"[SCIENTIFIC ERROR] {e}")

        elif choice == '3':
            calc.matrix_operation()

        elif choice == '4':
            calc.unit_converter()

        elif choice == '5':
            calc.history.display_history()

        elif choice == '6':
            print("\nThank you for using Advanced Calculator. Exiting...")
            break
        else:
            print("[ERROR] Invalid choice! Please select between 1 and 6.")

if __name__ == "__main__":
    main()