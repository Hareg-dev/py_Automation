import string
import random
import qrcode
from PIL import Image
from functools import wraps
import os

# Decorator for input validation
def validate_input(func):
    """Ensures inputs are valid, catching ValueError."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError:
            print("Invalid input! Please enter a number.")
            return None, None  # Return None for length and qr_choice if invalid
    return wrapper

# Decorator for confirmation
def confirm_action(prompt):
    """Confirms user intent before proceeding."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = input(prompt)
            if response != "1":  # Proceed if not '1'
                return func(*args, **kwargs)
            print("Action skipped.")
            return None
        return wrapper
    return decorator

# Decorator to log password generation
def log_generation(func):
    """Logs generated passwords to history."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        password = func(self, *args, **kwargs)
        if password and len(self._history) >= self._max_history:
            self._history.pop(0)
        if password:
            self._history.append(password)
        return password
    return wrapper

# Base class for PasswordGenerator with encapsulation
class PasswordGenerator:
    def __init__(self, custom_chars=None, min_length=6, max_length=20):
        # Encapsulation: private attributes
        self._characters = list(custom_chars or (string.ascii_letters + string.digits + "!@#$%^&*()"))
        self._password = ""  # Current password
        self._history = []   # Protected history
        self._max_history = 5
        self._min_length = min_length
        self._max_length = max_length

    @validate_input
    def get_user_input(self):
        """Gets user input with validation."""
        length = int(input("Please enter the number of digits for your password: "))
        qr_code = input("Do you want a QR code? (Enter '1' for yes): ")
        return length, qr_code

    @log_generation
    def generate_password(self, length):
        """Generates a password with length constraints."""
        if length < self._min_length:
            print(f"Length increased to minimum: {self._min_length}")
            length = self._min_length
        elif length > self._max_length:
            print(f"Length reduced to maximum: {self._max_length}")
            length = self._max_length
        self._password = "".join(random.choice(self._characters) for _ in range(length))
        return self._password

    def create_qr_code(self, filename="password.png", fill="blue", back="white"):
        """Creates and saves a QR code for the current password."""
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, border=3, box_size=6)
        qr.add_data(self._password)
        qr.make(fit=True)
        img = qr.make_image(fill=fill, back_color=back)
        img.save(filename)
        return img

    # Encapsulation: public getters
    def get_password(self):
        return self._password

    def get_history(self):
        return self._history.copy()  # Return a copy to protect internal state

# Polymorphic PasswordChecker base class
class PasswordChecker:
    def check(self, password):
        """Abstract method for checking passwords."""
        raise NotImplementedError("Subclasses must implement check()")

class PasswordStrengthChecker(PasswordChecker):
    def check(self, password):
        """Checks password strength based on criteria."""
        score = 0
        if len(password) >= 8: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()" for c in password): score += 1
        return "Strong" if score >= 4 else "Moderate" if score >= 2 else "Weak"

class PasswordLengthChecker(PasswordChecker):
    def check(self, password):
        """Checks password length."""
        if len(password) < 6: return "Too short"
        elif len(password) > 20: return "Too long"
        else: return "Good length"

# Enhanced subclass with custom behavior
class SecurePasswordGenerator(PasswordGenerator):
    def __init__(self, custom_chars=None):
        super().__init__(custom_chars=custom_chars, min_length=8)  
        self._fill_color = "purple"  

    def generate_password(self, length):
        """Overrides to ensure at least one of each character type."""
        password = super().generate_password(length)
        if not (any(c.isupper() for c in password) and any(c.isdigit() for c in password) and 
                any(c in "!@#$%^&*()" for c in password)):
            return self.generate_password(length) 
        return password

    def create_qr_code(self, filename="password.png"):
        """Custom QR code with purple fill."""
        return super().create_qr_code(filename=filename, fill=self._fill_color)

# Main execution with decorator
@confirm_action("Generate a password? (Anything except '1' to proceed): ")
def run_generator(generator):
    """Runs the generator and checks the password."""
    length, qr_choice = generator.get_user_input()
    if length is None: 
        return
    password = generator.generate_password(length)
    print("Your password:", password)

    if qr_choice == "1":
        qr_name = input("Enter QR filename (default 'password.png'): ") or "password.png"
        qr_img = generator.create_qr_code(qr_name)
        qr_img.show()
        if os.path.exists(qr_name):
            print(f"QR saved at: {os.path.abspath(qr_name)}")

    checkers = [PasswordStrengthChecker(), PasswordLengthChecker()]
    for checker in checkers:
        print(f"{checker.__class__.__name__}: {checker.check(password)}")
    print("Password history:", generator.get_history())

# Execute with enhancements
if __name__ == "__main__":
    custom = input("Custom characters (or Enter for default): ")
    generator_type = input("Secure (1) or Basic (2) generator? (1/2): ")
    generator = SecurePasswordGenerator(custom) if generator_type == "1" else PasswordGenerator(custom)
    
    while True:
        run_generator(generator)
        again = input("Another? (Enter '1' to stop): ")
        if again == "1":
            break
    print("Goodbye!")