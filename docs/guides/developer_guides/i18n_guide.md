# Internationalization (i18n) Guide

## Overview
This guide explains how to add and manage translations for the ThinkAlike project to support multiple languages.

## Directory Structure
- `locales/`: Contains translation files for each language.
  - Example: `locales/en/LC_MESSAGES/messages.po`

## Adding a New Language
1. Create a directory for the new language:
   ```
   mkdir -p locales/<language_code>/LC_MESSAGES
   ```
2. Create a `.po` file for the language:
   ```
   touch locales/<language_code>/LC_MESSAGES/messages.po
   ```
3. Add translations to the `.po` file.

## Updating Translations
1. Extract new messages:
   ```
   pybabel extract -o locales/messages.pot src/
   ```
2. Update `.po` files:
   ```
   pybabel update -d locales -i locales/messages.pot
   ```
3. Compile translations:
   ```
   pybabel compile -d locales
   ```

## Using Translations in Code
Use the `i18n.gettext` method to fetch translations:
```python
from src.i18n.i18n_config import i18n
print(i18n.gettext("es", "Welcome to ThinkAlike!"))
```
