---
title: "Практикум по разарботке ML"
author: "Анисимов Я.О и ко"
institute: "ИТМО"
theme: "Frankfurt"
colortheme: "beaver"
fonttheme: "professionalfonts"
fontsize: 11pt
urlcolor: red
linkstyle: bold
aspectratio: 169
titlegraphic: img/aleph0.png
logo: img/aleph0-small.png
date:
section-titles: false
toc: true
---

# Задача №4: прогнозирование возраста участников обследования по здоровью и питанию

## Описание задачи

Национальное обследование по здоровью и питанию (NHANES), проводимое Центрами по контролю и профилактике заболеваний (CDC), собирает обширную информацию о здоровье и питании разнообразного населения США. Датасет NHANES обычно слишком широк для конкретных аналитических целей. В данном поднаборе данных мы сужаем наш фокус на прогнозировании возраста участников, извлекая подмножество признаков из более крупного датасета NHANES. Эти выбранные признаки включают физиологические измерения, образ жизни и биохимические маркеры, которые, как предполагается, имеют сильную корреляцию с возрастом.

Ваша задача - создать модель машинного обучения для прогнозирования возраста участников национального обследования по здоровью и питанию (NHANES) на основе предоставленных признаков.

## ML задачи

- провести входной анализ данных (EDA)
- определить метрики для оценки эффективности модели
- сформировть baseline-модель
- предложить улучшенную модель и вывести ее в продакшн

## Описание датасета

Датасет включает в себя информацию о физиологических измерениях, образе жизни и биохимических маркерах участников обследования.
Участники разделены на две категории: `Senior` (возраст 65 лет и старше) и `Adult` (моложе 65 лет). Количество записей - 6287, признаков - 9. Целевая переменная - `age_group`.

__Примечание__: признак `RIDAGEYR` представляет собой возраст участников исследования. Очевидно его нельзя использовать для построения модели классификации по возрастным категориям. Однако вы можете построить регрессионную модель, тогда `RIDAGEYR` будет целевой переменной, а признак `age_group` исключается из тренировочного набора.
Если вы решите взять задачу регрессии - сообщите об этом преподавателю.

## Ссылка на датасет

[dataset4.zip](./dataset4.zip) (29 KB)