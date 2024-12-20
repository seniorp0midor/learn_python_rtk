import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns
import numpy as np
import pandas as pd
import sqlite3

data = pd.read_csv('Steam_2024_bestRevenue_1500.csv')
conn = sqlite3.connect('steam_database_2.db')

# Распределение жанров по продажам
def genre_sales_distribution(data):
    genre_sales = data.groupby('publisherClass')['revenue'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    genre_sales.plot(kind='bar', color='skyblue')
    plt.title('Продажи по классу издателя')
    plt.xlabel('Жанр')
    plt.ylabel('Общий доход ($)')
    plt.xticks(rotation=45)
    plt.show()

    genre_sales_df = genre_sales.reset_index()
    genre_sales_df.columns = ['Genre', 'TotalRevenue']
    genre_sales_df.to_sql('GenreSales', conn, if_exists='replace', index=False)

# Корреляция цены и объема продаж
def price_sales_correlation(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='price', y='copiesSold', data=data, color='orange')
    plt.title('Цена vs Объем продаж')
    plt.xlabel('Цена ($)')
    plt.ylabel('Проданные копии')
    plt.show()

    price_sales_df = data[['price', 'copiesSold']].copy()
    price_sales_df.to_sql('PriceSales', conn, if_exists='replace', index=False)

# Корреляция рейтинга и продаж
def rating_sales_correlation(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='reviewScore', y='copiesSold', data=data, color='green')
    plt.title('Рейтинг vs Объем продаж')
    plt.xlabel('Оценка')
    plt.ylabel('Проданные копии')
    plt.show()

    rating_sales_df = data[['reviewScore', 'copiesSold']].copy()
    rating_sales_df.to_sql('RatingSales', conn, if_exists='replace', index=False)

# Влияние событий продаж (на основе даты выхода)
def seasonal_sales_impact(data):
    data['releaseDate'] = pd.to_datetime(data['releaseDate'], format='%d-%m-%Y')
    data['year'] = data['releaseDate'].dt.year
    data['month'] = data['releaseDate'].dt.month
    monthly_sales = data.groupby('month')['copiesSold'].sum()
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='line', marker='o', color='blue')
    plt.title('Тренды продаж по месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Общий объем продаж')
    plt.xticks(np.arange(1, 13), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
    plt.show()

    monthly_sales_df = monthly_sales.reset_index()
    monthly_sales_df.columns = ['Month', 'TotalSales']
    monthly_sales_df.to_sql('MonthlySales', conn, if_exists='replace', index=False)

# Строим графики
genre_sales_distribution(data)
price_sales_correlation(data)
rating_sales_correlation(data)
seasonal_sales_impact(data)

# Дополнительные данные о доходах игр
data2 = {
    'Game': [
        'WWE 2K24',
        'Shin Megami Tensei V: Vengeance',
        'KINGDOM HEARTS -HD 1.5+2.5 ReMIX-',
        'Legend of Mortal',
        'Backpack Battles',
        'EA SPORTS™ Madden NFL 25',
        'Soulmask',
        'Pixel Gun 3D: PC Edition'
    ],
    'Revenue': [
        8.05,
        7.6,
        6.8,
        7.76,
        4.66,
        3.18,
        0,
        0
    ],
    'Review Score': [
        0,
        96,
        0,
        0,
        0,
        0,
        79,
        62
    ],
    'Type': [
        'AAA',
        'AAA',
        'AAA',
        'Indie',
        'Indie',
        'AAA',
        'Indie',
        'Indie'
    ]
}
df = pd.DataFrame(data2)
df = df[df['Revenue'] > 0]

plt.figure(figsize=(12, 6))
sns.barplot(x='Game', y='Revenue', hue='Type', data=df)
plt.title('Доходы игр (AAA vs Indie)')
plt.xticks(rotation=45)
plt.ylabel('Доход (в миллионах)')
plt.xlabel('Игры')
plt.legend(title='Тип игры')
plt.tight_layout()
plt.show()
df.to_sql('GameRevenue', conn, if_exists='replace', index=False)

conn.close()

