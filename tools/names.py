import random
from datetime import datetime, timedelta
from pprint import pprint


random_dates = []

for i in range(10000):
    random_dates.append(datetime.fromtimestamp(random.randint(0, 2**32)).strftime('%Y-%m-%d'))

# Base lists of first names, last names, and father names in Russian and Kazakh languages.
# These lists are simplified and may not cover the full range of names found in Kazakhstan.
russian_first_names = ['Алексей', 'Дмитрий', 'Максим', 'Иван', 'Кирилл', 'Сергей', 'Владимир', 'Николай', 'Егор', 'Артем']
russian_last_names = ['Иванов', 'Петров', 'Сидоров', 'Николаев', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков']
russian_father_names = ['Алексеевич', 'Дмитриевич', 'Максимович', 'Иванович', 'Кириллович', 'Сергеевич', 'Владимирович', 'Николаевич', 'Егорович', 'Артемович', None]

kazakh_first_names = ['Аслан', 'Бауыржан', 'Ғалым', 'Даурен', 'Ерлан', 'Жасұлан', 'Заңғар', 'Ильяс', 'Қайрат', 'Мұрат']

kazakh_last_names = ['Нұрғалиев', 'Саттаров', 'Темиров', 'Ұразбаев', 'Фазылов', 'Хасенов', 'Чекенов', 'Шарипов', 'Ермеков', 'Юсупов']

kazakh_father_names = ['Асланұлы', 'Бауыржанұлы', 'Ғалымұлы', 'Дауренұлы', 'Ерланұлы', 'Жасұланұлы', 'Заңғарұлы', 'Ильясұлы', 'Қайратұлы', 'Мұратұлы', None]

addresses = [ "ул. Абая, д. 10, кв. 25, г. Алматы, Казахстан", "ул. Ленина, д. 45, г. Нур-Султан, Казахстан", "ул. Байтурсынова, д. 7, кв. 12, г. Шымкент, Казахстан", "ул. Сатпаева, д. 3, г. Караганда, Казахстан", "ул. Достык, д. 22, кв. 8, г. Актобе, Казахстан", "ул. Желтоксан, д. 60, г. Атырау, Казахстан", "ул. Макатаева, д. 18, кв. 3, г. Павлодар, Казахстан", "ул. Толе би, д. 9, г. Усть-Каменогорск, Казахстан", "ул. Шевченко, д. 14, кв. 31, г. Семей, Казахстан", "ул. Торайгырова, д. 38, г. Костанай, Казахстан", "ул. Алтынсарина, д. 5, кв. 2, г. Кызылорда, Казахстан", "ул. Гоголя, д. 11, г. Уральск, Казахстан", "ул. Жамбыла, д. 7, кв. 18, г. Петропавловск, Казахстан", "ул. Абдирова, д. 33, г. Актау, Казахстан", "ул. Мичурина, д. 29, г. Тараз, Казахстан", "ул. Ауэзова, д. 17, кв. 22, г. Степногорск, Казахстан", "ул. Сейфуллина, д. 12, г. Аягоз, Казахстан", "ул. Бектурова, д. 20, г. Есик, Казахстан", "ул. Байсеитова, д. 6, кв. 15, г. Жезказган, Казахстан", "ул. Абжаева, д. 25, г. Темиртау, Казахстан", "ул. Магжана, д. 9, г. Туркестан, Казахстан", "ул. Динмухамеда, д. 14, кв. 8, г. Кокшетау, Казахстан", "ул. Муканова, д. 30, г. Рудный, Казахстан", "ул. Сарайшык, д. 11, г. Аксай, Казахстан", "ул. Курмангазы, д. 17, кв. 12, г. Экибастуз, Казахстан", "ул. Сатубалдина, д. 21, г. Аркалык, Казахстан", "ул. Темирлана, д. 8, г. Шахтинск, Казахстан", "ул. Макенжулы, д. 4, кв. 27, г. Талдыкорган, Казахстан", "ул. Каныша Сатпаева, д. 6, г. Сарань, Казахстан", "ул. Бокеева, д. 12, г. Атбасар, Казахстан", "ул. Алтынай, д. 18, кв. 7, г. Жанаозен, Казахстан", "ул. Толеген, д. 5, г. Текели, Казахстан", "ул. Айтеке, д. 10, г. Кентау, Казахстан", "ул. Алмазар, д. 22, кв. 15, г. Балхаш, Казахстан", "ул. Жулдыза, д. 7, г. Лисаковск, Казахстан", "ул. Куралай, д. 14, кв. 9, г. Жаркент, Казахстан", "ул. Туран, д. 18, г. Аральск, Казахстан", "ул. Кайрат, д. 9, кв. 23, г. Тараз, Казахстан", "ул. Акколь, д. 30, г. Шалкар, Казахстан", "ул. Достык, д. 12, г. Сарыагаш, Казахстан", "ул. Женис, д. 25, г. Бейнеу, Казахстан", "ул. Кокшетау, д. 8, кв. 11, г. Житикара, Казахстан", "ул. Маметова, д. 17, г. Аркасу, Казахстан", "ул. Толе би, д. 5, г. Октябрьское, Казахстан", ]

addresses = [address.split(",")[0:2] for address in addresses]
addresses = [", ".join(address) for address in addresses]
print(addresses)

ad = russian_first_names + kazakh_first_names
add = russian_last_names + kazakh_last_names
adf = russian_father_names + kazakh_father_names

# Generating lists
def generate_names(first_names, last_names, father_names, count=100):
    names_list = []
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        father_name = random.choice(father_names)
        full_name = [first_name, last_name, father_name]  # Father name may be None
        names_list.append(full_name)
    return names_list

def generate_phone_number():
    return f"+7{random.randint(7000000000, 7999999999)}"

def generate_udo(count: int = 12):
    random_date = random.choice(random_dates)
    if random_date.split("-")[0] > "2015":
        return generate_udo() 
    # generate 9 random number
    return "".join([str(random.randint(0, 9)) for _ in range(9)]), random.choice(random_dates), random.choice(["МВД", "МИД"])


# Generate for both languages
russian_names = generate_names(ad, add, adf, 10000)

gender = ['Мужчина', 'Женщина']

grand = "Казахстан"


print(generate_udo())
