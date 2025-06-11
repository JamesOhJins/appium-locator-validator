# 📌 appium-locator-validator

`appium-locator-validator` is a lightweight static analysis tool for Appium test automation repositories.  
It scans all Python files starting with `el_` (e.g. `el_main_page.py`, `el_login_screen.py`) and validates that each locator follows best practices and formatting rules.

This tool is ideal for enforcing consistent locator definitions across teams and CI environments.

---

## ✅ What It Checks

- Locator variable names must be **UPPERCASE**
- Locators must be defined as tuples like:  
  ```python
  LOCATOR_NAME = (AppiumBy.METHOD, "selector string")
The AppiumBy.METHOD must be valid (e.g., ID, XPATH, CLASS_NAME, etc.)

The selector string must pass method-specific validation:

XPATH must start with //

CLASS_NAME must start with android. or XCUIElement

ANDROID_UIAUTOMATOR must include ( and ) and be balanced

And more...

## 🧪 Examples

### ✅ Valid locators
```python
LOGIN_BUTTON = (AppiumBy.ID, "com.example:id/login")
SIGNUP_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='Sign up']")
TOOLBAR_ICON = (AppiumBy.ACCESSIBILITY_ID, "toolbar_icon")
```

### ❌ Invalid locators
```python
login_button = (AppiumBy.ID, "com.example:id/login")                     # lowercase name
MISSING_TUPLE = AppiumBy.ID, "com.example:id/forgot_password"           # not in a tuple
BAD_XPATH = (AppiumBy.XPATH, "android.widget.TextView[@text='Text']")  # missing leading '//'
WRONG_CLASS = (AppiumBy.CLASS_NAME, "Button")                           # doesn't start with android. or XCUIElement
BROKEN_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, "UiSelector.text(\"Login\")")  # unbalanced or invalid
```

## 📋 Example Output
```bash
🔍 Scanning file: ./loc/android/el_mirror_page.py

❌ Locator validation errors found:
./el_locator.py:4: Locator name 'lowercase_locator' is not in uppercase. -> 
lowercase_locator = (AppiumBy.ID, 'this is a id')

./el_locator.py:5: Invalid selector value for method ID -> 
MALFORMED_LOCATOR = (AppiumBy.ID, 'this is a id', 'extra_value')

./el_locator.py:6: Invalid selector value for method ANDROID_UIAUTOMATOR -> 
MALFORMED_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'ID')

./loc/android/el_mirror_page.py:11: Locator name 'login_button' is not in uppercase. -> 
login_button = (AppiumBy.ID, "com.example:id/login")

./loc/android/el_mirror_page.py:13: Invalid selector value for method XPATH -> 
BAD_XPATH = (AppiumBy.XPATH, "android.widget.TextView[@text='MissingSlash']")

./loc/android/el_mirror_page.py:14: Invalid selector value for method CLASS_NAME -> 
WRONG_CLASS = (AppiumBy.CLASS_NAME, "Button")

./loc/android/el_mirror_page.py:15: Could not parse locator value -> 
BROKEN_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, "UiSelector.text(\"Login\")")

Execution time: 0.01 seconds
```