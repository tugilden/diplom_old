import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mainalgo import mainalgo
import numpy as np

# Получение данных из функции mainalgo
points, df_old, df = mainalgo()

# Разделение координат x и y из заданных точек
x = [vec[0] for vec in points]
y = [vec[1] for vec in points]

# Извлечение коэффициентов alpha, beta, gamma из исходных и новых данных
alpha_old = df_old["alpha"].tolist()
beta_old = df_old["beta"].tolist()
gamma_old = df_old["gamma"].tolist()

alpha = df["alpha"].tolist()
beta = df["beta"].tolist()
gamma = df["gamma"].tolist()

# Определение границ для графика
left_edge = min(x) - 20
right_edge = max(x) + 20

# Создание объектов трасс (trace) для прямых по старым и новым коэффициентам
traces_old = []
traces_new = []

# Генерация значений x и вычисление соответствующих y для старых коэффициентов
for i in range(len(alpha_old)):
   x_vals = np.linspace(left_edge, right_edge, 100)
   y_vals_old = (-alpha_old[i] * x_vals + gamma_old[i]) / beta_old[i]
   
   trace_old = go.Scatter(
       x=x_vals,
       y=y_vals_old,
       mode='lines',
       name=f'Линия {i+1}',
       line=dict(color='blue')
   )
   traces_old.append(trace_old)

# Генерация значений x и вычисление соответствующих y для новых коэффициентов
for i in range(len(alpha)):
   x_vals = np.linspace(left_edge, right_edge, 100)
   y_vals_new = (-alpha[i] * x_vals + gamma[i]) / beta[i]
   
   trace_new = go.Scatter(
       x=x_vals,
       y=y_vals_new,
       mode='lines',
       name=f'Линия {i+1}',
       line=dict(color='green')
   )
   traces_new.append(trace_new)

# Создание объекта трасс (trace) для отображения точек
trace1 = go.Scatter(
   x=x,
   y=y,
   mode='lines+markers',
   marker=dict(size=10, color='blue'),
   line=dict(color='red', width=2),
   name='Точки'
)

# Создание подграфика для отображения графиков
fig = make_subplots(rows=1, cols=1)

# Добавление всех трасс на график
for trace in traces_old + traces_new:
   fig.add_trace(trace, row=1, col=1)

# Добавление трасс для отображения точек на графике
fig.add_trace(trace1, row=1, col=1)

# Настройка кнопок для переключения между графиками
fig.update_layout(
   xaxis_title="X",
   yaxis_title="Y",
   updatemenus=[
       dict(
           buttons=list([
               dict(label="Старые линии",
                    method="update",
                    args=[{"visible": [True]*len(traces_old) + [False]*len(traces_new) + [False]},
                          {"title": "Прямые до выкидывания"}]),
               dict(label="Новые линии",
                    method="update",
                    args=[{"visible": [False]*len(traces_old) + [True]*len(traces_new) + [False]},
                          {"title": "Прямые после выкидывания"}]),
               dict(label="Точки",
                    method="update",
                    args=[{"visible": [False]*len(traces_old) + [True]*len(traces_new) + [True]},
                          {"title": "Точки после работы алгоритма"}])
           ]),
           direction="down",
           showactive=True,
           x=0.5,
           xanchor="center",
           y=1.1,
           yanchor="top"
       ),
   ]
)

# Начальная видимость трасс на графике
fig.update_traces(visible=False)

# Отображение графика при нажатии на кнопку
fig.show()
