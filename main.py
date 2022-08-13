from util import verify_phone_number, verify_email_address, get_contact_by_name
from storage import read_contacts, write_contacts


CONTACT_FILE_PATH = "contacts.json"


def add_contact(contacts):
    first_name = input("Имя: ").lower().strip()
    last_name = input("Фамилия: ").lower().strip()
    mobile = input("Номер телефона: ").strip()
    home = input("Номер домашнего телефона: ").strip()
    email = input("Электронная почта: ").strip()
    address = input("Адрес: ").strip()

    if not first_name or not last_name:
        print("Контактное лицо должно иметь имя и фамилию.")
    elif mobile and not verify_phone_number(mobile):
        print("Неверный номер мобильного телефона.")
    elif home and not verify_phone_number(home):
        print("Неверный номер домашнего телефона.")
    elif email and not verify_email_address(email):
        print("Неверный адрес электронной почты.")
    elif get_contact_by_name(first_name, last_name, contacts):
        print("Контакт с таким именем уже существует.")
    else:
        new_contact = {
            "first_name": first_name,
            "last_name": last_name,
            "mobile": mobile,
            "home": home,
            "email": email,
            "address": address
        }
        contacts.append(new_contact)
        print("Контакт Добавлен!")
        return

    print("Вы ввели неверную информацию, этот контакт не был добавлен.")


def search_for_contact(contacts):
    first_name_search_string = input("Имя").lower().strip()
    last_name_search_string = input("Фамилия: ").lower().strip()

    matching_contacts = []
    for contact in contacts:
        first_name = contact["first_name"]
        last_name = contact["last_name"]

        if first_name_search_string and first_name_search_string not in first_name:
            continue
        if last_name_search_string and last_name_search_string not in last_name:
            continue

        matching_contacts.append(contact)

    print(f"Найдено {len(matching_contacts)} совпадающих контактов.")
    list_contacts(matching_contacts)


def delete_contact(contacts):
    first_name = input("Имя: ").lower().strip()
    last_name = input("Фамилия: ").lower().strip()

    contact = get_contact_by_name(first_name, last_name, contacts)
    if not contact:
        print("Никаких контактов с этим именем не существует.")
    else:
        confirm = input("Вы уверены, что хотите удалить этот контакт (y/n)? ").lower()
        if confirm == "y": 
            contacts.remove(contact)
            print("Контакт удален!")
    

def get_contact_string(contact):
    string = f'{contact["first_name"].capitalize()} {contact["last_name"].capitalize()}'

    for field in ["mobile", "home", "email", "address"]:
        value = contact[field]
        if not value:
            continue

        string += f"\n\t{field.capitalize()}: {value}"

    return string


def list_contacts(contacts):
    sorted_contacts = sorted(contacts, key=lambda x: x['first_name'])

    for i, contact in enumerate(sorted_contacts):
        print(f"{i + 1}. {get_contact_string(contact)}")


def main(contacts_path):
    print("Добро пожаловать в ваш список контактов!\n")
    print("Ниже приведен список используемых команд:")
    print("\"add\": Добавить контакт.")
    print("\"delete\": Удалить контакт.")
    print("\"list\": Вывести список контактов.")
    print("\"search\": Поиск контакта по имени.")
    print("\"q\": Выйти из программы и сохранить изменения.\n")

    contacts = read_contacts(contacts_path)

    while True:
        command = input("Введите команду ").lower().strip()

        if command == "q":
            write_contacts(contacts_path, contacts)
            print("Контакты были успешно сохранены.")
            break
        elif command == "add":
            add_contact(contacts)
        elif command == "delete":
            delete_contact(contacts)
        elif command == "list":
            list_contacts(contacts)
        elif command == "search":
            search_for_contact(contacts)
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main(CONTACT_FILE_PATH)
