
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            print("Contact not found.")
        except IndexError:
            print("Enter user name")
        except TypeError:
            print("Invalid input. Please check your input.")
    return wrapper


CONTACTS = {}


@input_error
def handle_hello():
    print("How can I help you?")


@input_error
def handle_add(name, phone):
    if name in CONTACTS.keys():
        print("Contact already exists.")
    else:
        CONTACTS[name] = phone
        print(f"Contact {name} added with phone number {phone}")


@input_error
def handle_change(name, phone):
    if name in CONTACTS.keys():
        CONTACTS[name] = phone
        print(f"Phone number for contact {name} changed to {phone}")
    else:
        raise KeyError


@input_error
def handle_phone(name):
    print(f"The phone number for contact {name} is {CONTACTS[name]}")


@input_error
def handle_show_all():
    if len(CONTACTS) == 0:
        raise KeyError
    else:
        for name, phone in CONTACTS.items():
            print("".join(f"{name}: {phone}"))


def handle_bye():
    print("Good bye!")
    exit()


COMMANDS = {
    "hello": handle_hello,
    "add": handle_add,
    "change": handle_change,
    "phone": handle_phone,
    "show all": handle_show_all,
    'good bye': handle_bye,
    'close': handle_bye,
    'exit': handle_bye,
}


@input_error
def main():
    while True:
        user_input = input("Enter a command: ").lower()
        if user_input.find('.') != -1:
            break

        for command in COMMANDS.keys():
            if user_input.startswith(command):
                args = user_input[len(command):].split()
                if len(args) == 0:
                    COMMANDS[command]()
                elif len(args) == 1:
                    COMMANDS[command](args[0])
                elif len(args) == 2:
                    COMMANDS[command](args[0], args[1])
                else:
                    COMMANDS[command](args)
                break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
