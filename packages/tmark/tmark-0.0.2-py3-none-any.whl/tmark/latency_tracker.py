import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Table:
    def __init__(self, label):
        self.label = label
        self.starts_times = np.array([])
        self.end_times = np.array([])
        self.latencies = np.array([])
        self.timestamps = np.array([])

    def matrix(self):
        return np.vstack([self.starts_times, self.end_times, self.latencies, self.timestamps])


class LatencyTracker:
    def __init__(self):
        self.labels = np.array([])
        self.data = np.array([])
        self.t0 = time.time()


    def start(self, label: str) -> None:
        """
        Фиксирует время начала выполнения участка кода с указанной меткой.
        """
        index = np.where(label == self.labels)[0]
        if not index.shape == (0,):
            self.data[index[0]].starts_times = np.hstack([self.data[index[0]].starts_times, time.time() - self.t0])
        else:
            self.labels = np.hstack([self.labels, label])
            self.data = np.hstack([self.data, Table(label)])
            self.data[-1].starts_times = np.hstack([self.data[-1].starts_times, time.time() - self.t0])

    def stop(self, label: str) -> None:
        """
        Фиксирует время окончания выполнения участка кода с указанной меткой и вычисляет задержку.
        """
        end_time = time.time() - self.t0
        index = np.where(label == self.labels)[0]
        if not index.shape == (0,):
            item = index[0]
        else:
            item = -1
        self.data[item].end_times = np.hstack([self.data[item].end_times, end_time])
        # Вычисляем задержку и сохраняем её
        latency = end_time - self.data[item].starts_times[-1]
        self.data[item].latencies = np.hstack([self.data[item].latencies, latency])

        # Сохраняем текущее время для оси X
        self.data[item].timestamps = np.hstack([self.data[item].timestamps, end_time])

    def plot(self) -> None:
        """
        Строит графики задержек для каждой метки.
        """
        plt.figure()
        for index_table, table in enumerate(self.data):
            m = table.matrix()
            plt.plot(m[3], m[2], marker='o', label=f"{table.label}")

        plt.xlabel('Время [с]')
        plt.ylabel('Задержка [с]')
        plt.title('График задержек по времени для разных меток')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_from_csv(self, path: str = './csv/'):
        """
        Строим график из всех файлов внутри папки с csv файлами, объединяя их
        """
        import os
        files = os.listdir(path)
        print(files)
        plt.figure()
        for file in files:
            df = pd.read_csv(f'{path}{file}', index_col=0)
            plt.plot(df['t'], df['latencies'], label=f'{file}', marker='o')
        plt.xlabel('Time [s]')
        plt.ylabel('Latency [s]')
        plt.title('Latencies')
        plt.legend()
        plt.grid(True)
        plt.show()

    def save_to_numpy(self, path: str = './numpy/') -> None:
        """
        Сохранение в npy файл всего массива
        :param path:
        :return:
        """
        import numpy as np
        from os.path import isdir
        if not isdir(path):
            from os import mkdir
            mkdir('numpy')
        array = self.vstack_data()
        np.save(f'{path}data.npy', array[1:])

    def vstack_data(self):
        array = np.zeros(self.data[0].starts_times.shape)
        for table in self.data:
            array = np.vstack([array, table.matrix()])
        return array[1:]

    def save_to_csv(self, path: str = './csv/') -> None:
        from os.path import isdir
        if not isdir(path):
            from os import mkdir
            mkdir('csv')
        for table in self.data:
            df = pd.DataFrame(table.matrix().T, columns=[f'starts_times',
                                                         f'end_times',
                                                         f'latencies',
                                                         f't'])
            df.to_csv(f'{path}data_{table.label}.csv')

    def get_labels(self) -> np.ndarray:
        labels = np.array([])
        for table in self.data:
            labels = np.hstack([labels, table.label])
        return labels
