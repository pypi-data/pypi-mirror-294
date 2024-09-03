# Описание
Данный модуль предназначен для установки временных меток в коде, удобно использовать в циклах.

```python
import tmark as tm
import time

tracker = tm.LatencyTracker()

# Имитация выполнения цикла с несколькими метками в одной итерации
for i in range(4):
    tracker.start("operation_1")
    time.sleep(0.1 + i * 0.02)  # Симуляция первой операции
    tracker.stop("operation_1")

    tracker.start("operation_2")
    time.sleep(0.2 + i * 0.03)  # Симуляция второй операции
    tracker.stop("operation_2")

    tracker.start("operation_3")
    time.sleep(0.15 + i * 0.01)  # Симуляция третьей операции
    tracker.stop("operation_3")
    
# Сохранение в csv файл
tracker.save_to_csv()

# Чтение из csv файла и построение графика
tracker.plot_from_csv()
```
![alt text](img.png "Title")