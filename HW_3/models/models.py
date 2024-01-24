import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier


df = pd.read_csv('/content/pricerunner_aggregate.csv')
df.head(5)
df.shape
df.info()
pd.set_option('display.float_format', lambda x:'%.3f'%x)
df.describe(include='all')
df.isnull().sum()
df.duplicated().sum()

df.hist(bins=30, figsize=(15, 10))
plt.show()
corr_matrix = df.corr(numeric_only=True)
corr_matrix
plt.subplots(figsize=(15,8))
fig=sns.heatmap(corr_matrix, annot=True, square=True, cmap=sns.cubehelix_palette(as_cmap=True), fmt='.4g')
fig


df.columns = ['Product_ID', 'Product_Title', 'Merchant_ID', 'Cluster_ID',
              'Cluster_Label', 'Category_ID', 'Category_Label']
df.head(1)
df.head(1)
df['Product_ID'].is_unique
df = df.set_index('Product_ID')
df.head(5)
df.head(1)
df['Product_Title'].describe()

df['Product_Title'].nunique()
df['Product_Title'].value_counts()
# ### 30 самых популярных продуктов
top30_product = df['Product_Title'].value_counts(dropna=False).nlargest(30)
top30_product
# ## 3. **Merchant ID** - Идентификатор продавца
df.head(1)
# ### Количество уникальных позиций
# Кол-во уникальных позиций
df['Merchant_ID'].nunique()
df['Merchant_ID'].value_counts()
# График распределения топ 30 продкутов в зависимости от продовцов
_df = df[df['Product_Title'].isin(top30_product.index)]
profession_ranking = list(top30_product.index)

f, ax = plt.subplots(figsize=(12,5))
ax = sns.boxenplot(x="Product_Title", y="Merchant_ID",
              color="gray",  palette="Set3", order=profession_ranking,
              scale="linear", data=_df, linewidth=0.5)

ax.tick_params(axis='x', rotation=90)
ax.set_title("Топ 30 продкутов в зависимости от продовцовв", fontsize=14)

means = _df.groupby("Product_Title")["Merchant_ID"].mean().loc[profession_ranking]
_ = plt.plot(range(len(profession_ranking)), means, marker="o", color="green", markersize=6, linestyle="--")
# ## 4. **Cluster_ID**	- Идентификатор кластера
df.head(1)
# ### Количество уникальных позиций
# Кол-во уникальных позиций
df['Cluster_ID'].nunique()
df['Cluster_ID'].value_counts()
# ## 4. **Cluster_Label**	- Наименование
df.head(1)
# ### Количество уникальных позиций
# Кол-во уникальных товаров
df['Cluster_Label'].nunique()
df['Cluster_Label'].value_counts()
# 30 самых популярных продуктов
top30_prod = df['Cluster_Label'].value_counts(dropna=False).nlargest(30)
top30_prod
# ## 6. **Category_ID** - Идентификатор категории
df.head(1)
# Кол-во уникальных товаров
df['Category_ID'].nunique()
df['Category_ID'].value_counts()
# ## На графике
sns.barplot(
    x=df["Category_ID"].value_counts().index,
    y=df["Category_ID"].value_counts())
plt.show()
# **Вывод:**
# 
# Как видно, есть небольшой дисбаланс классов. Есть категории, в которых по кол-ву более чем в 2 раза меньше значений.
# ## 7. **Category_Label** - Наименование категории
df.head(1)
# Кол-во уникальных товаров
df['Category_Label'].nunique()
df['Category_Label'].value_counts()
# ## На графике
sns.barplot(
    x=df["Category_Label"].value_counts().index,
    y=df["Category_Label"].value_counts())

plt.xticks(rotation=60)
plt.show()
# ## Проверка других столбцов на схожесть
df['Cluster_ID'].nunique()
df['Cluster_Label'].nunique()
df = pd.read_csv('/content/pricerunner_aggregate.csv')
df.columns = ['Product_ID', 'Product_Title', 'Merchant_ID', 'Cluster_ID',
              'Cluster_Label', 'Category_ID', 'Category_Label']
df = df.set_index('Product_ID')

df['Product_Title'] = df['Product_Title'].str.lower()

category_id_unique = df['Category_ID'].unique()
for i in range(len(category_id_unique)):
  df['Category_ID'] = df['Category_ID'].replace({category_id_unique[i]: i+1})
df.shape
df.sample(10)
df['Product_Title'] = df['Product_Title'].str.lower()
category_id_unique = df['Category_ID'].unique()
category_id_unique
for i in range(len(category_id_unique)):
  df['Category_ID'] = df['Category_ID'].replace({category_id_unique[i]: i+1})
df.sample(10)
category_dict = dict(zip(df['Category_ID'], df['Category_Label']))
category_dict
RANDOM_STATE = 42
X = df["Product_Title"]
Y = df["Category_ID"]

print(X.shape)
print(Y.shape)
# Разделение на обучающую и проверочную выборки в соотношении 80/20.
x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=RANDOM_STATE)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
# ### TfIdf
tfidf = TfidfVectorizer(
    max_features=10000, stop_words="english", ngram_range=(1, 4), lowercase=True
)
x_train = tfidf.fit_transform(x_train)
x_test = tfidf.transform(x_test)

print(x_train.shape)
print(x_test.shape)
# ### Сохранение
with open("tfidf.pkl", "wb") as file:
    pickle.dump(tfidf, file)
# ## Model 1 - logistic regression
log_reg = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
log_reg.fit(x_train, y_train)
print(classification_report(y_test, log_reg.predict(x_test)))
# Сохранение
with open("log_reg.pkl", "wb") as file:
    pickle.dump(log_reg, file)
# ## Model 2 - Naive Bayes
naive_bayes = MultinomialNB()
naive_bayes.fit(x_train, y_train)
print(classification_report(y_test, naive_bayes.predict(x_test)))
# Сохранение
with open("naive_bayes.pkl", "wb") as file:
    pickle.dump(naive_bayes, file)
# ## Model 3 - CatBoost
from google.colab import output
output.enable_custom_widget_manager()
catboost = CatBoostClassifier(
    random_seed=RANDOM_STATE,
    iterations=1000,
    depth=5,
    learning_rate=0.15,
    eval_metric="TotalF1",
    use_best_model=True,
    task_type="GPU",
    devices="0:1",
)
catboost.fit(x_train, y_train, eval_set=(x_test, y_test), verbose=500, plot=True)
print(classification_report(y_test, catboost.predict(x_test)))
with open("catboost.pkl", "wb") as file:
    pickle.dump(catboost, file)

X_encoded = pd.get_dummies(X)
x_train, X_test, Y_train,Y_test = train_test_split(X_encoded, Y, test_size=0.2, random_state=42)
forest = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
forest.fit(pd.DataFrame(X_train), Y_train)

pred_forest = forest.predict(X_test)
acc_forest = accuracy_score(Y_test, pred_forest)
print(acc_forest)
df.to_csv('processed_pricerunner_aggregate.csv')