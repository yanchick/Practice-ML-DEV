import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from joblib import dump

def load_and_process_data():
    # Загрузка данных
    data = pd.read_csv('TCGA_GBM_LGG_Mutations_all.csv')

    # Проверка на наличие пропущенных значений
    print(data.isnull().sum())

    # Преобразование категориальных переменных в числовые
    le = LabelEncoder()
    for column in data.columns:
        if data[column].dtype == type(object):
            data[column] = le.fit_transform(data[column])

    # Визуализация распределения целевой переменной
    sns.countplot(data['Grade'])
    plt.show()

    # Визуализация корреляции признаков
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    plt.show()

    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data.drop('Grade', axis=1)
    X.columns = [col.lower() for col in X.columns]  # Приведение имен столбцов к нижнему регистру
    y = data['Grade']


    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Нормализация признаков
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Сохранение LabelEncoder и StandardScaler
    dump(le, 'label_encoder.joblib')
    dump(scaler, 'scaler.joblib')

    return X_train_scaled, X_test_scaled, y_train, y_test
