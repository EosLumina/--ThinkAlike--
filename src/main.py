from src.i18n.i18n_config import i18n

def main():
    user_language = "es"  # Example: dynamically detect or set user language
    print(i18n.gettext(user_language, "Welcome to ThinkAlike!"))
    print(i18n.gettext(user_language, "Find meaningful social connections based on shared values."))

if __name__ == "__main__":
    main()
