# This file contains valid and invalid locators for testing purposes.
from appium.webdriver.common.appiumby import AppiumBy

# Valid locators
LOGIN_BUTTON = (AppiumBy.ID, "com.example:id/login")
SIGNUP_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='Sign up']")
TOOLBAR_ICON = (AppiumBy.ACCESSIBILITY_ID, "toolbar_icon")

# Invalid locators
login_button = (AppiumBy.ID, "com.example:id/login")
MISSING_TUPLE = AppiumBy.ID, "com.example:id/forgot_password"
BAD_XPATH = (AppiumBy.XPATH, "android.widget.TextView[@text='MissingSlash']")
WRONG_CLASS = (AppiumBy.CLASS_NAME, "Button")
BROKEN_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, "UiSelector.text(\"Login\")")
