import pandas as pd
import numpy as np
from algo import algorithm


def find_intersection_point(line1, line2):
    D = line1["alpha"] * line2["beta"] - line2["alpha"] * line1["beta"]
    Dx = line1["gamma"] * line2["beta"] - line2["gamma"] * line1["beta"]
    Dy = line1["alpha"] * line2["gamma"] - line2["alpha"] * line1["gamma"]
    
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return "Прямые параллельны или совпадают, точек пересечения нет"


def check_row(df, row):
    '''Проверяет является ли избыточным неравенство [k]
    Возвращает True, если является. Используется в buble()'''
    # Проверяем, чтобы избежать деления на ноль
    if row["beta"] == 0:
        # Для строки с β = 0, используем другую проверку
        # Если β = 0, то уравнение вида αx ≤ γ
        # Просто возвращаем False чтобы не удалять
        return False
    
    # Для обычного случая
    try:
        a = df["alpha"] - df["beta"] * row["alpha"] / row["beta"]
        b = df["gamma"] - df["beta"] * row["gamma"] / row["beta"]

        mmax = 150000
        mmin = -mmax
        for i, _ in a.items():
            if a[i] < 0:
                mmin = max(mmin, b[i] / a[i])
            elif a[i] > 0:
                mmax = min(mmax, b[i] / a[i])
        if mmax <= mmin:
            return True
        else: 
            return False
    except:
        # Если возникла ошибка, считаем, что неравенство не избыточно
        return False


def buble(df):
    '''Прямой поиск и удаление неравенств-следствий.
    Трудоемкость - квадратичная.'''
    for index, row in df.iterrows():
        if check_row(df, row):
            df.drop(index, axis=0, inplace=True)
    return df


def vec_numbering(df):
    basic_vec = np.array([1, 0])
    basic_vec_norm = 1
    degrees = dict()

    for index, row in df.iterrows():
        vec = np.array([row["alpha"], row["beta"]])

        scalar_product = np.dot(basic_vec, vec)
        vec_norm = np.linalg.norm(vec)
        cosine_angle = scalar_product / (vec_norm * basic_vec_norm)
        angle = np.arccos(cosine_angle)

        if row["beta"] < 0:
            angle = 2*np.pi - angle

        degrees[index] = angle

    return degrees


def is_area(x, y, df):
    for _, row in df.iterrows():
        if row["alpha"] * x + row["beta"] * y > row["gamma"]:
            return False
    return True


def mainalgo():
    # Считываем файл
    df_old = pd.read_csv('./halfplane.csv')
    # Выкидывыаем ненужные прямые
    df = df_old.copy()
    df = buble(df)

    # Нумерация векторов
    degrees = vec_numbering(df)
    sortred_vectors = [tup[0] for tup in sorted(degrees.items(), key=lambda item: item[1])]

    # Обход точек
    Points = []
    flag = False
    new_line = 0

    for i in range(len(sortred_vectors)):
        if flag:
            line1 = new_line
            flag = False
        else:
            line1 = df.loc[sortred_vectors[i]]
        if i == len(sortred_vectors) - 1:
            line2 = df.loc[sortred_vectors[0]]
        else:
            line2 = df.loc[sortred_vectors[i+1]]

        result = find_intersection_point(line1, line2)
        if isinstance(result, tuple):
            x, y = result
        else:
            # Пропускаем параллельные прямые
            continue

        if x % 1 == 0 and y % 1 == 0:
            Points.append(np.array([x, y]))
            continue
        else:
            tmp_points = algorithm(line1, line2)
            for i in range(len(tmp_points)):
                x = tmp_points[i][0]
                y = tmp_points[i][1]
                if is_area(x, y, df):
                    Points.append(tmp_points[i])
                else:
                    if len(Points) != 0:
                        alpha = y - Points[-1][1]
                        beta = Points[-1][0] - x
                        if alpha == 0:
                            beta = 1
                            gamma = y
                        elif beta == 0:
                            alpha = 1
                            gamma = x
                        else:
                            gamma = alpha * Points[-1][0] - beta * Points[-1][1]
                        data = {'alpha': alpha,
                            'beta': beta,
                            'gamma': gamma}
                        new_line = pd.Series(data)
                        flag = True

    return Points, df_old, df