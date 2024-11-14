# загружаем все библиотеки для работы
# с данными и построения графиков
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

# отключаем предупреждения в консоли
warnings.filterwarnings('ignore')

# устанавливаем параметры изображения
# показываем все столбцы
pd.set_option('display.max_columns', None)
# задаём ширину таблицы в 1 000 пикселей
pd.set_option('display.width', 1000)
# ограничиваем вывод первыми 15 строками
pd.set_option('display.max_rows', 10)

# указываем путь к нашему файлу
file_path = 'Marvel Vs DC NEW.csv'
# считываем данные
df = pd.read_csv(file_path)

# задаём ключевые слова для поиска фильмов Marvel
marvel_keywords = [
    "Avengers", "Black Panther", "Captain America", "Doctor Strange", "Eternals",
    "Falcon", "Guardians of the Galaxy", "Hawkeye", "Hulk", "Iron Man", "Loki",
    "Scarlet Witch", "Shang-Chi", "Spider-Man", "Thor", "WandaVision", "Ant-Man",
    "Black Widow", "Captain Marvel", "Deadpool", "X-Men", "Wolverine", "Fantastic Four",
    "Ms. Marvel", "Moon Knight", "She-Hulk", "Daredevil", "Punisher", "Jessica Jones",
    "Luke Cage", "Iron Fist", "Inhumans", "What If...?", "Mutant X", "Secret Invasion", "Blade",
    "Agents of S.H.I.E.L.D.",
    "Fantastic 4"
]

# задаём ключевые слова для поиска фильмов DC
dc_keywords = [
    "Batman", "Superman", "Wonder Woman", "Aquaman", "Flash", "Green Lantern",
    "Joker", "Shazam", "Justice League", "Suicide Squad", "Harley Quinn", "Batwoman",
    "Arrow", "Supergirl", "Doom Patrol", "Titans", "Black Adam", "Peacemaker",
    "Constantine", "Swamp Thing", "Watchmen", "Green Arrow", "Blue Beetle",
    "Hawkman", "Zatanna", "Catwoman", "Cyborg", "Teen Titans", "Darkseid", "Smallvile"
]


# создаём функцию классификации
def classify_movie(title):
    # проверяем, есть ли в заголовке ключевые слова фильмов Marvel
    for keyword in marvel_keywords:
        # если такие есть, маркируем фильм как Marvel
        if keyword in title:
            return 'Marvel'
    # проверяем, есть ли в заголовке ключевые слова фильмов DC
    for keyword in dc_keywords:
        # если такие есть, маркируем фильм как DC
        if keyword in title:
            return 'DC'
    # если в названии нет таких слов, возвращаем значение Unknown
    return 'Unknown'


# применяем функцию к столбцу с названием Movie
# и создаём новый столбец Franchise
df['Franchise'] = df['Movie'].apply(classify_movie)

# выводим на экран в консоли первые 10 фильмов
print('\nВыводим датасет после классификации по франшизам')
print(df.head(10))

# удаляем столбец с описанием фильмов
df = df.drop(columns=['Description'])
# создаём отдельный датафрейм для фильмов с отметкой Unknown
unknown_franchise = df[df['Franchise'] == 'Unknown']
# выводим первые 5 фильмов для проверки
print('\nВыводим датасет с фильмами без франшиз')
print(unknown_franchise.head())

# фильтруем данные: оставляем только те строки, где рейтинг IMDb не равен 0
df = df[df['IMDB_Score'] != 0]
# фильтруем данные: удаляем все, где столбец Franchise = Unknown
df = df[df['Franchise'] != 'Unknown']
# выводим первые 5 фильмов для проверки
print('\nВыводим датасет после фильтрации от нулевого рейтинга и неизвестной франшизы')
print(df.head())

# строим график 1: уникальные фильмы
# удаляем дублирующиеся фильмы из датасета
# и сохраняем результат в переменной df_unique
df_unique = df.drop_duplicates(subset='Movie')
# используя метод value_counts(), подсчитываем
# количество уникальных фильмов для обеих франшиз
franchise_counts = df_unique['Franchise'].value_counts()

# указываем в дюймах размер будущего графика
plt.figure(figsize=(8, 6))
# строим столбчатую диаграмму kind='bar'
franchise_counts.plot(kind='bar', color=['blue', 'red'])
# устанавливаем заголовок и размер шрифта для заголовка
plt.title('Сравниваем количество уникальных фильмов Marvel и DC', fontsize=16)
# устанавливаем называния для осей и размер шрифта
plt.xlabel('Франшиза', fontsize=12)
plt.ylabel('Количество уникальных фильмов', fontsize=12)
# устанавливаем поворот названия для оси X в ноль градусов
plt.xticks(rotation=0)
# отрисовываем график
plt.show()

# строим график 2: средний рейтинг фильмов
# группируем фильмы по франшизам и вычисляем средний рейтинг
average_ratings = df_unique.groupby('Franchise')['IMDB_Score'].mean()

# строим столбчатую диаграмму kind='bar'
average_ratings.plot(kind='bar', color=['blue', 'red'], figsize=(10, 8))
# устанавливаем подпись для всего графика
plt.title('Средний IMDb-рейтинг для фильмов Marvel и DC')
# устанавливаем подпись для оси Y
plt.ylabel('Средний IMDb-рейтинг')
# устанавливаем поворот меток на оси X в 35 градусов для лучшей читаемости
plt.xticks(rotation=35)
# отрисовываем график
plt.show()

# строим график 3: количество фильмов Marvel и DC по годам
# подсчитываем количество фильмов для каждой комбинации год-франшиза
movies_per_year = df_unique.groupby(['Year', 'Franchise']).size().unstack().fillna(0)

# строим линейный график: по оси X идут годы, по Y — количество фильмов
movies_per_year.plot(kind='line', figsize=(10, 8))
# устанавливаем название графика
plt.title('Производство фильмов DC и Marvel по годам')
# устанавливаем название оси X
plt.xlabel('Год')
# устанавливаем название оси Y
plt.ylabel('Количество фильмов')
# устанавливаем поворот меток на оси X в 35 градусов для лучшей читаемости
plt.xticks(rotation=35)
# отрисовываем график
plt.show()
<<<<<<< HEAD
=======

# строим график 4: фильмы с высоким рейтингом IMDb
# фильтруем данные: оставляем только фильмы с рейтингом от 8.0 и выше
top_movies = df_unique[df_unique['IMDB_Score'] >= 8.0]
>>>>>>> b0d01fb (initial loading and charting)
