import pickle
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(str(p) for p in self.phones)
        bday = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Name: {self.name}, Phones: {phones}{bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join([str(record) for record in self.data.values()])

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()

    while True:
        user_input = input("Enter a command (add, change, show, all, save, exit): ").strip().lower()
        if user_input == "exit":
            break
        elif user_input == "save":
            save_data(book)
            print("Data saved successfully.")
        elif user_input == "all":
            print(book)
        elif user_input.startswith("add"):
            try:
                name, phone = user_input.split()[1:3]
                record = book.find(name)
                if record is None:
                    record = Record(name)
                    book.add_record(record)
                record.add_phone(phone)
                print(f"Added phone {phone} to {name}.")
            except ValueError as e:
                print(f"Error: {e}. Make sure to provide a name and phone number.")
            except IndexError:
                print("Error: 'add' command requires a name and phone number.")
        elif user_input.startswith("change"):
            try:
                name, old_phone, new_phone = user_input.split()[1:4]
                record = book.find(name)
                if record:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Changed {old_phone} to {new_phone} for {name}.")
                else:
                    print(f"Error: Contact {name} not found.")
            except ValueError as e:
                print(f"Error: {e}. Make sure the phone number format is correct.")
            except IndexError:
                print("Error: 'change' command requires a name, old phone, and new phone.")
        elif user_input == "show":
            name = input("Enter name to show phones: ")
            record = book.find(name)
            if record:
                print(f"Phones for {name}: {', '.join(p.value for p in record.phones)}")
            else:
                print(f"Contact {name} not found.")
        else:
            print("Unknown command.")

    save_data(book)

if __name__ == "__main__":
    main()
