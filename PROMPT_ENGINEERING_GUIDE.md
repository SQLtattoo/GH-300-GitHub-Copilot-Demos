# 🎯 Prompt Engineering Guide for GitHub Copilot

**Audience:** Developers  
**Purpose:** Learn to write effective prompts that generate high-quality code with GitHub Copilot  
**Duration:** 20-30 minute read with hands-on practice

---

## 📋 Table of Contents

1. [The 4Ss: Core Principles](#the-4ss-core-principles)
2. [Basic Prompt Structure](#basic-prompt-structure)
3. [Prompt Crafting Techniques](#prompt-crafting-techniques)
4. [Comment-Driven Development](#comment-driven-development)
5. [Context is King](#context-is-king)
6. [Function & Method Naming](#function--method-naming)
7. [Iterative Refinement](#iterative-refinement)
8. [Advanced Techniques](#advanced-techniques)
9. [Common Patterns](#common-patterns)
10. [Anti-Patterns (What NOT to Do)](#anti-patterns-what-not-to-do)
11. [Practice Exercises](#practice-exercises)

---

## The 4Ss: Core Principles

Before we explore specific strategies, let's first understand the basic principles of prompt engineering, summed up in the **4 Ss** below. These core rules are the basis for creating effective prompts with GitHub Copilot.

### 1. **Single**
Always focus your prompt on a single, well-defined task or question. This clarity is crucial for eliciting accurate and useful responses from Copilot.

```python
# ❌ Multiple tasks: Trying to do too much at once
# Create a user, validate their email, send a welcome message, and log the activity

# ✅ Single task: One clear, focused action
# Create a new user in the database with the given email and name
def create_user(email: str, name: str) -> User:
```

### 2. **Specific**
Ensure that your instructions are explicit and detailed. Specificity leads to more applicable and precise code suggestions.

```python
# ❌ Vague: What kind of validation? What rules?
# Validate the password

# ✅ Specific: Explicit requirements and constraints
# Validate password: min 8 chars, at least one uppercase, one lowercase, 
# one digit, and one special character (!@#$%^&*)
def validate_password(password: str) -> bool:
```

### 3. **Short**
While being specific, keep prompts concise and to the point. This balance ensures clarity without overloading Copilot or complicating the interaction.

```python
# ❌ Too verbose: Excessive explanation dilutes the intent
# I would like you to please create a function that will take a number 
# and then check if that number is even or not and then return the result
# as a boolean value indicating whether it's even

# ✅ Short and clear: Essential information only
# Return True if n is even, False otherwise
def is_even(n: int) -> bool:
```

### 4. **Surround**
Utilize descriptive filenames and keep related files open. This provides Copilot with rich context, leading to more tailored code suggestions.

```python
# ✅ Copilot reads context from:
# - Current file: user_repository.py
# - Open files: user.py (User model), database.py (DB connection)
# - Existing patterns in the file

class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by ID from database."""
        # Copilot sees the User model and database patterns
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db.execute(query, (user_id,))
        return User(**result) if result else None
    
    # When you start typing the next method, Copilot uses the surrounding
    # context to suggest consistent patterns and return types
    def get_by_email(self, email: str) -> Optional[User]:
```

**Pro Tip:** Keep your workspace organized with descriptive filenames like `user_repository.py`, `order_service.py`, or `payment_validator.py`. Copilot uses these names to understand your intent.

---

## Basic Prompt Structure

A well-structured prompt helps GitHub Copilot understand exactly what you need. Great prompts often contain up to four elements:

| Element | Purpose | Example |
|---------|---------|---------|
| **Instruction** | What you want Copilot to do | "Calculate the compound interest" |
| **Context** | Background or constraints | "for a savings account with monthly compounding" |
| **Input** | The data to process | "given principal, rate, and time in years" |
| **Output Format** | How the result should be presented | "return as a float rounded to 2 decimal places" |

### Putting It All Together

```python
# Instruction: Calculate the compound interest
# Context: for a savings account with monthly compounding (12 times per year)
# Input: principal amount, annual interest rate (as decimal), and time in years
# Output: return the final amount as a float rounded to 2 decimal places
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
```

**Result:** Copilot generates accurate code with the formula `A = P(1 + r/n)^(nt)`.

### Quick Reference: The 4 Elements in Action

```python
# [INSTRUCTION] Validate an email address
# [CONTEXT] using regex pattern matching for standard email format
# [INPUT] email string to validate
# [OUTPUT] return True if valid, False otherwise; do not raise exceptions
def is_valid_email(email: str) -> bool:
```

> 💡 **Tip:** You don't always need all four elements. Simple tasks may only require an instruction, while complex operations benefit from the full structure.

---

## Prompt Crafting Techniques

### 1. **Be Specific, Not Generic**

❌ **Bad Prompt:**
```python
# Calculate something
def process():
```

✅ **Good Prompt:**
```python
# Calculate the total shipping cost based on weight (kg), distance (km), 
# and shipping type (standard or express). Express costs 2x standard rate.
def calculate_shipping_cost(weight: float, distance: float, is_express: bool) -> float:
```

**Why it works:** Copilot understands the business logic, units, and pricing rules.

---

### 2. **Include Edge Cases in Comments**

❌ **Bad Prompt:**
```python
# Divide two numbers
def divide(a, b):
```

✅ **Good Prompt:**
```python
# Divide a by b. Raise ValueError if b is zero.
# Return result rounded to 2 decimal places.
def divide(a: float, b: float) -> float:
```

**Result:** Copilot generates defensive code with proper error handling.

---

### 3. **Specify Data Types & Return Values**

❌ **Bad Prompt:**
```python
# Get user info
def get_user():
```

✅ **Good Prompt:**
```python
# Fetch user data from the database by user_id.
# Returns dict with keys: 'name', 'email', 'created_at'.
# Returns None if user not found.
def get_user(user_id: int) -> Optional[Dict[str, Any]]:
```

**Why it works:** Type hints + comment description = better suggestions.

---

## Comment-Driven Development

### The Power of Descriptive Comments

Copilot reads comments above your code to understand intent. Write comments as specifications.

### Pattern: Step-by-Step Algorithm

✅ **Effective Pattern:**
```python
def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters long
    - Contains uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character (!@#$%^&*)
    
    Returns True if valid, False otherwise.
    """
    # Copilot will implement all requirements
```

**Result:** Copilot generates complete validation logic checking all criteria.

---

### Pattern: Example-Driven Development

✅ **Show Examples:**
```python
# Parse a date string in multiple formats and return a datetime object.
# Examples:
#   "2025-12-17" -> datetime(2025, 12, 17)
#   "12/17/2025" -> datetime(2025, 12, 17)
#   "Dec 17, 2025" -> datetime(2025, 12, 17)
# Raise ValueError if format is not recognized.
def parse_flexible_date(date_str: str) -> datetime:
```

**Why it works:** Examples clarify ambiguous requirements.

---

## Context is King

Copilot reads surrounding code to understand patterns. Use this to your advantage.

### Pattern: Establish Convention First

```python
class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by ID from database."""
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db.execute(query, (user_id,))
        return User(**result) if result else None
    
    # Copilot will now follow the same pattern for new methods!
    def get_by_email(self, email: str) -> Optional[User]:
        # Copilot suggests: query, execute, return pattern
```

**Result:** Consistent code style across all repository methods.

---

### Pattern: Show the Pattern, Get More

```python
# Existing code establishes pattern
def add(self, a: float, b: float) -> float:
    """Add two numbers and return the result."""
    result = a + b
    self.history.append(f"add({a}, {b}) = {result}")
    return result

def subtract(self, a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    result = a - b
    self.history.append(f"subtract({a}, {b}) = {result}")
    return result

# Now just type the signature for multiply
def multiply(self, a: float, b: float) -> float:
    # Copilot automatically includes docstring AND history tracking!
```

---

## Function & Method Naming

Names are prompts! Descriptive names generate better code.

### Naming Strategies

❌ **Vague Names:**
```python
def process(data):      # What kind of processing?
def handle(item):       # Handle how?
def do_stuff(x, y):     # What stuff?
```

✅ **Descriptive Names:**
```python
def sanitize_user_input(raw_input: str) -> str:
    # Copilot knows to remove HTML, SQL injection attempts, etc.

def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    # Copilot generates the compound interest formula

def retry_on_network_failure(func: Callable, max_attempts: int = 3):
    # Copilot creates retry logic with exponential backoff
```

---

### Verb-Noun Pattern

Use clear verb-noun combinations:

| Pattern | Example | Copilot Understands |
|---------|---------|---------------------|
| `get_*` | `get_user_profile()` | Fetch/retrieve operation |
| `set_*` | `set_cache_timeout()` | Update/modify operation |
| `is_*` / `has_*` | `is_valid_email()` | Boolean check, returns True/False |
| `calculate_*` | `calculate_tax()` | Math/computation operation |
| `parse_*` | `parse_json_config()` | Convert from one format to another |
| `validate_*` | `validate_credit_card()` | Check rules, return bool or raise error |
| `format_*` | `format_currency()` | Transform data for display |

---

## Iterative Refinement

You don't need the perfect prompt on the first try. Iterate!

### Technique: Start Broad, Then Narrow

**Iteration 1:**
```python
# Sort a list of users
def sort_users(users):
```

**Iteration 2:** (Add constraints)
```python
# Sort a list of user dictionaries by 'last_login' date, most recent first
def sort_users(users: List[Dict]) -> List[Dict]:
```

**Iteration 3:** (Add edge cases)
```python
# Sort a list of user dictionaries by 'last_login' date, most recent first.
# Users with no 'last_login' should appear at the end.
# Handle None values gracefully.
def sort_users(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
```

---

### Technique: Use Chat for Complex Requirements

For complex logic, use Copilot Chat to refine:

```
👤 "Generate a function that validates a JSON schema with custom error messages"

🤖 [Copilot generates basic version]

👤 "Add support for nested objects and array validation"

🤖 [Copilot refines with nested support]

👤 "Include line numbers in error messages"

🤖 [Copilot adds line tracking]
```

---

## Advanced Techniques

### 1. **Multi-Line Comment Blocks**

For complex functions, use detailed docstrings:

```python
def process_payment(
    user_id: int,
    amount: float,
    payment_method: str,
    currency: str = "USD"
) -> Dict[str, Any]:
    """
    Process a payment transaction with fraud detection.
    
    Workflow:
    1. Validate user exists and is active
    2. Check payment method is valid and not expired
    3. Run fraud detection algorithm
    4. If fraud score > 0.8, flag for manual review
    5. Process payment through payment gateway
    6. Update user balance and transaction history
    7. Send confirmation email
    
    Args:
        user_id: Database ID of the user
        amount: Payment amount (must be positive)
        payment_method: One of ['credit_card', 'paypal', 'bank_transfer']
        currency: ISO currency code (default: USD)
    
    Returns:
        Dict containing:
            - transaction_id: str
            - status: str ('success', 'pending', 'failed')
            - fraud_score: float (0.0 to 1.0)
            - timestamp: datetime
    
    Raises:
        ValueError: If amount is negative or zero
        UserNotFoundError: If user_id doesn't exist
        PaymentGatewayError: If external payment service fails
    """
    # Copilot generates comprehensive implementation following all steps!
```

---

### 2. **Inline Examples in Comments**

```python
def format_phone_number(phone: str) -> str:
    """
    Format phone number to international standard.
    
    Input formats accepted:
        "1234567890" -> "+1 (123) 456-7890"
        "123-456-7890" -> "+1 (123) 456-7890"
        "+11234567890" -> "+1 (123) 456-7890"
    
    Assumes US numbers if no country code provided.
    """
    # Copilot handles all format variations
```

---

### 3. **Context Through Test Cases**

Write test first, implementation second:

```python
def test_calculate_fibonacci():
    """Test Fibonacci sequence generation."""
    assert fibonacci(0) == []
    assert fibonacci(1) == [0]
    assert fibonacci(5) == [0, 1, 1, 2, 3]
    assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Now implement - Copilot knows the exact requirements from tests!
def fibonacci(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    # Copilot generates code that passes all tests above
```

---

### 4. **Reference External Patterns**

```python
# Implement the Builder pattern for creating User objects
# Similar to how we built the PaymentBuilder class in payment.py
class UserBuilder:
```

**Why it works:** Copilot can reference other files in your workspace.

---

## Common Patterns

### Pattern 1: Data Transformation Pipeline

```python
# Transform raw CSV data through multiple stages:
# 1. Parse CSV into list of dicts
# 2. Filter out rows where 'status' != 'active'
# 3. Convert 'created_at' strings to datetime objects
# 4. Sort by 'priority' (high to low)
# 5. Return top 10 results
def process_customer_data(csv_path: str) -> List[Dict[str, Any]]:
```

---

### Pattern 2: Error Handling Template

```python
def fetch_api_data(url: str, retries: int = 3) -> Dict:
    """
    Fetch data from external API with retry logic.
    
    Retry on: ConnectionError, Timeout (with exponential backoff)
    Don't retry on: 4xx errors (client errors)
    Log all attempts and failures.
    Raise custom APIError after all retries exhausted.
    """
    # Copilot generates robust error handling
```

---

### Pattern 3: Configuration Object

```python
# Create a configuration validator that:
# - Loads from YAML file
# - Validates required keys: ['database', 'cache', 'logging']
# - Provides default values for optional keys
# - Raises ConfigError with helpful message if validation fails
# - Returns a typed ConfigObject with dot notation access (config.database.host)
class ConfigLoader:
```

---

## Anti-Patterns (What NOT to Do)

### ❌ 1. **Too Vague**

```python
# Do the thing
def process():
```

**Problem:** Copilot has no context about what "thing" is.

---

### ❌ 2. **Conflicting Information**

```python
# Return a list of users
def get_user() -> User:  # Says list, returns User???
```

**Problem:** Comment and signature contradict each other.

---

### ❌ 3. **No Context in Isolation**

```python
# In a file with no other code:
def helper():  # What does it help with?
```

**Problem:** No surrounding code to establish patterns.

---

### ❌ 4. **Overly Generic Names**

```python
def util(x):     # Utility for what?
def manager():   # Manages what?
def data(obj):   # What kind of data?
```

**Problem:** Names provide zero semantic meaning.

---

### ❌ 5. **Incomplete Type Hints**

```python
def process(items):  # items is what? List? Dict? Custom class?
    return items
```

**Better:**
```python
def process_orders(items: List[Order]) -> List[ProcessedOrder]:
```

---

## Practice Exercises

Try these prompts in the demo project to see Copilot in action:

### Exercise 1: Basic Function
```python
# Calculate the area of a circle given its radius.
# Use π = 3.14159. Return result rounded to 2 decimal places.
def calculate_circle_area(radius: float) -> float:
```

---

### Exercise 2: Data Validation
```python
# Validate an email address format.
# Must contain @ symbol, domain name, and valid TLD (.com, .org, etc.)
# Return True if valid, False otherwise.
# Examples: "user@example.com" -> True, "invalid.email" -> False
def is_valid_email(email: str) -> bool:
```

---

### Exercise 3: Complex Logic
```python
# Parse a log file and extract error messages.
# Each line format: "TIMESTAMP [LEVEL] MESSAGE"
# Return list of tuples: [(timestamp, message), ...]
# Only include lines where LEVEL is "ERROR"
# Skip malformed lines without raising exceptions
def parse_error_logs(log_file_path: str) -> List[Tuple[str, str]]:
```

---

### Exercise 4: API Integration
```python
# Fetch weather data from OpenWeather API for a given city.
# Return dict with: temperature (celsius), humidity (%), description
# Handle API errors gracefully, return None on failure
# Cache results for 5 minutes to avoid excessive API calls
def get_weather(city: str, api_key: str) -> Optional[Dict[str, Any]]:
```

---

### Exercise 5: Test-Driven
```python
# Write tests first:
def test_merge_sorted_lists():
    assert merge_sorted_lists([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted_lists([], [1, 2]) == [1, 2]
    assert merge_sorted_lists([1], []) == [1]
    assert merge_sorted_lists([], []) == []

# Now implement - let Copilot use the tests as specification
def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:
    """Merge two sorted lists into one sorted list."""
```

---

## 🎯 Key Takeaways

1. **Be Specific** - Detailed prompts = better code
2. **Use Type Hints** - Help Copilot understand data structures
3. **Provide Examples** - Show input/output expectations
4. **Establish Patterns** - Surrounding code teaches Copilot your style
5. **Iterate** - Refine prompts based on initial suggestions
6. **Name Intentionally** - Function names are prompts themselves
7. **Document Edge Cases** - Error handling and boundaries matter
8. **Use Tests as Specs** - Write tests, let Copilot implement

---

## 📚 Additional Resources

- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- Practice with the demo project: `src/calculator.py`, `src/data_processor.py`

---

## 🚀 Next Steps

1. **Practice** - Complete the exercises above in the demo project
2. **Experiment** - Try different prompt styles for the same function
3. **Compare** - See how prompt changes affect Copilot's suggestions
4. **Apply** - Use these techniques in your real projects

**Remember:** Prompt engineering is a skill that improves with practice. Start with these patterns and develop your own style over time!

---

