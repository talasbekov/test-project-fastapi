import random

# Base lists of first names, last names, and father names in Russian and Kazakh languages.
# These lists are simplified and may not cover the full range of names found in Kazakhstan.
russian_first_names = ['Алексей', 'Дмитрий', 'Максим', 'Иван', 'Кирилл', 'Сергей', 'Владимир', 'Николай', 'Егор', 'Артем']
russian_last_names = ['Иванов', 'Петров', 'Сидоров', 'Николаев', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков']
russian_father_names = ['Алексеевич', 'Дмитриевич', 'Максимович', 'Иванович', 'Кириллович', 'Сергеевич', 'Владимирович', 'Николаевич', 'Егорович', 'Артемович', None]

kazakh_first_names = ['Аслан', 'Бауыржан', 'Ғалым', 'Даурен', 'Ерлан', 'Жасұлан', 'Заңғар', 'Ильяс', 'Қайрат', 'Мұрат']

kazakh_last_names = ['Нұрғалиев', 'Саттаров', 'Темиров', 'Ұразбаев', 'Фазылов', 'Хасенов', 'Чекенов', 'Шарипов', 'Ермеков', 'Юсупов']

kazakh_father_names = ['Асланұлы', 'Бауыржанұлы', 'Ғалымұлы', 'Дауренұлы', 'Ерланұлы', 'Жасұланұлы', 'Заңғарұлы', 'Ильясұлы', 'Қайратұлы', 'Мұратұлы', None]


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
from pprint import pprint

# Generate for both languages
russian_names = generate_names(ad, add, adf, 10000)



