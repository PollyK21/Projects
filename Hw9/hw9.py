
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Contact"
        except TypeError:
            return "Invalid input. Please check your input."
    return wrapper


CONTACTS = {}


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add(name, phone):
    if name not in CONTACTS.keys():
        CONTACTS[name] = phone
        return f"Contact {name} added with phone number {phone}"
    else:
        return "Contact already exists."


@input_error
def handle_change(name, phone):
    if name in CONTACTS.keys():
        CONTACTS[name] = phone
        return f"Phone number for contact {name} changed to {phone}"
    else:
        raise KeyError


@input_error
def handle_phone(name):
    return f"The phone number for contact {name} is {CONTACTS[name]}"


@input_error
def handle_show_all():
    if len(CONTACTS) == 0:
        raise KeyError
    else:
        for name, phone in CONTACTS.items():
            return "".join(f"{name}: {phone}")


COMMANDS = {
    "hello": handle_hello,
    "add": handle_add,
    "change": handle_change,
    "phone": handle_phone,
    "show all": handle_show_all
}


@input_error
def main():
    while True:
        user_input = input("Enter a command: ").lower()
        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        for command in COMMANDS.keys():
            if user_input.startswith(command):
                args = user_input[len(command):].split()
                print(COMMANDS[command](*args))
                break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
