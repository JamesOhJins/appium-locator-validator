import ast
import os
import re
import time
from appium.webdriver.common.appiumby import AppiumBy

SUPPORTED_APPIUMBY_METHODS = {
    "ID",
    "XPATH",
    "ACCESSIBILITY_ID",
    "CLASS_NAME",
    "CSS_SELECTOR",
    "IOS_PREDICATE",
    "IOS_CLASS_CHAIN",
    "ANDROID_UIAUTOMATOR",
    "ANDROID_VIEWTAG",
    "ANDROID_DATA_MATCHER",
    "ANDROID_VIEW_MATCHER",
    "IMAGE",
    "CUSTOM",
    "FLUTTER_INTEGRATION_SEMANTICS_LABEL",
    "FLUTTER_INTEGRATION_TYPE",
    "FLUTTER_INTEGRATION_KEY",
    "FLUTTER_INTEGRATION_TEXT",
    "FLUTTER_INTEGRATION_TEXT_CONTAINING",
}

VALIDATORS = {
    # Ensure ID is a non-empty string
    "ID": lambda v: isinstance(v, str) and v.strip() != "",
    # Ensure XPATH starts with //
    "XPATH": lambda v: isinstance(v, str) and v.startswith("//"),
    # Ensure Accessibility ID is a non-empty string
    "ACCESSIBILITY_ID": lambda v: isinstance(v, str) and v.strip() != "",
    # Ensure Class Name is non-empty string
    "CLASS_NAME": lambda v: isinstance(v, str) and (v.startswith("android.") or v.startswith("XCUIElement")),
    # Ensure iOS Predicate contains ==
    "IOS_PREDICATE": lambda v: isinstance(v, str) and "==" in v,
    # Ensure iOS Class Chain starts with **
    "IOS_CLASS_CHAIN": lambda v: isinstance(v, str) and v.startswith("**/"),
    # Ensure Android UIAutomator has balanced parentheses and at least one method
    "ANDROID_UIAUTOMATOR": lambda v: isinstance(v, str) and v.count('(') == v.count(')') and v.count('(') >= 1,
    # IMAGE validation checks if the value is a string ending with .png or .jpg
    "IMAGE": lambda v: isinstance(v, str) and v.endswith((".png", ".jpg")),
    # below methods are not used in the project, only validates if they are strings
    "ANDROID_VIEWTAG": lambda v: isinstance(v, str),
    "ANDROID_DATA_MATCHER": lambda v: isinstance(v, str),
    "ANDROID_VIEW_MATCHER": lambda v: isinstance(v, str),
    "CUSTOM": lambda v: isinstance(v, str),
    "FLUTTER_INTEGRATION_SEMANTICS_LABEL": lambda v: isinstance(v, str),
    "FLUTTER_INTEGRATION_TYPE": lambda v: isinstance(v, str),
    "FLUTTER_INTEGRATION_KEY": lambda v: isinstance(v, str),
    "FLUTTER_INTEGRATION_TEXT": lambda v: isinstance(v, str),
    "FLUTTER_INTEGRATION_TEXT_CONTAINING": lambda v: isinstance(v, str),
}

LOCATOR_PATTERN = re.compile(
    r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\((AppiumBy\.[A-Z_]+)\s*,\s*([\'\"].+?[\'\"])\)'
)

def validate_locator(name, method, value):
    if not name.isupper():
        return f"Locator name '{name}' is not in uppercase."

    method_key = method.replace("AppiumBy.", "")
    if method_key not in SUPPORTED_APPIUMBY_METHODS:
        return f"Unsupported AppiumBy method"

    try:
        value_unquoted = ast.literal_eval(value)
    except Exception:
        return f"Could not parse locator value"

    if method_key in VALIDATORS and not VALIDATORS[method_key](value_unquoted):
        return f"Invalid selector value for method {method_key}"

    return None

def find_locators_in_file(filepath):
    errors = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, 1):
            match = LOCATOR_PATTERN.match(line.strip())
            if match:
                name, method, value = match.groups()
                error = validate_locator(name, method, value)
                if error:
                    errors.append((filepath, line_num, line.strip(), error))
    return errors

def find_el_files(base_dir="."):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.startswith("el_") and file.endswith(".py"):
                yield os.path.join(root, file)


if __name__ == "__main__":
    start_time = time.time()
    all_errors = []
    for file_path in find_el_files():
        print(f"🔍 Scanning file: {file_path}")
        file_errors = find_locators_in_file(file_path)
        if file_errors:
            all_errors.extend(file_errors)

    if all_errors:
        print("\n❌ Locator validation errors found:")
        for file_path, line_num, line, error in all_errors:
            print(f"{file_path}:{line_num}: {error} -> \n{line}\n")
        print(f"Execution time: {time.time() - start_time:.2f} seconds")
        exit(1)
    else:
        print("\n✅ All locators passed validation!")
        print(f"Execution time: {time.time() - start_time:.2f} seconds")
        exit(0)