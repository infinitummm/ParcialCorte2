import random
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class DataPointAgent(Agent):
    def __init__(self, unique_id, model, x, y, label):
        super().__init__(unique_id, model)
        self.x, self.y, self.label = x, y, label
        self.predicted_label = 0
        self.correctly_classified = False
        self.color = 'blue' if label == -1 else 'red'

    def update_classification(self, pred):
        self.predicted_label = pred
        self.correctly_classified = (self.label == pred)
        if self.correctly_classified:
            self.color = 'lightgreen' if self.label == -1 else 'lightcoral'
        else:
            self.color = 'darkblue' if self.label == -1 else 'darkred'


class PerceptronAgent(Agent):
    def __init__(self, uid, model, lr=0.1):
        super().__init__(uid, model)
        self.lr = lr
        self.weights = np.random.uniform(-1, 1, 2)
        self.bias = np.random.uniform(-1, 1)
        self.epoch = 0
        self.errors = []
        self.converged = False

    def step(self):
        total_error = 0
        for a in [ag for ag in self.model.schedule.agents if isinstance(ag, DataPointAgent)]:
            activation = self.weights[0]*a.x + self.weights[1]*a.y + self.bias
            pred = 1 if activation >= 0 else -1
            error = a.label - pred
            total_error += abs(error)
            if error != 0:
                self.weights[0] += self.lr * error * a.x
                self.weights[1] += self.lr * error * a.y
                self.bias += self.lr * error
            a.update_classification(pred)
        self.errors.append(total_error)
        self.epoch += 1
        if total_error == 0 or self.epoch >= self.model.max_iter:
            self.model.running = False

    def get_decision_boundary(self, x_range):
        # Retorna x, y de frontera de decisión
        if abs(self.weights[1]) > 1e-10:
            xs = np.linspace(x_range[0], x_range[1], 100)
            ys = -(self.weights[0]*xs + self.bias) / self.weights[1]
            return xs, ys
        # Vertical
        xs = np.full(100, -self.bias / self.weights[0] if abs(self.weights[0]) > 1e-10 else 0)
        ys = np.linspace(x_range[0], x_range[1], 100)
        return xs, ys


class PerceptronModel(Model):
    def __init__(self, n=50, lr=0.1, max_iter=100, rng=10):
        super().__init__()
        self.n_points = n
        self.max_iter = max_iter
        self.data_range = rng
        self.running = True
        self.schedule = RandomActivation(self)
        m, c = random.uniform(-1, 1), random.uniform(-rng/4, rng/4)
        for i in range(n):
            x, y = random.uniform(-rng, rng), random.uniform(-rng, rng)
            label = 1 if y > m*x + c else -1
            self.schedule.add(DataPointAgent(i+1, self, x, y, label))
        self.perc = PerceptronAgent(0, self, lr)
        self.schedule.add(self.perc)

    def step(self):
        if self.running:
            self.schedule.step()


class PerceptronUI:
    def __init__(self):
        self.model = None
        self.running = False
        self.root = tk.Tk()
        self.root.title('Perceptrón Mesa 0.8.9')
        self.root.geometry('1200x800')
        self._build()
        self.root.mainloop()

    def _build(self):
        frm = ttk.Frame(self.root)
        frm.pack(fill=tk.BOTH, expand=1)

        ctrl = ttk.LabelFrame(frm, text='Controles')
        ctrl.pack(fill=tk.X, pady=5)

        ttk.Label(ctrl, text='Tasa de Aprendizaje').grid(row=0, column=0)
        self.lr = tk.DoubleVar(value=0.1)
        ttk.Scale(ctrl, from_=0.01, to=1, variable=self.lr,
                  orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, padx=5)
        ttk.Label(ctrl, textvariable=self.lr).grid(row=0, column=2)

        ttk.Label(ctrl, text='Iteraciones').grid(row=1, column=0)
        self.it = tk.IntVar(value=100)
        ttk.Scale(ctrl, from_=10, to=500, variable=self.it,
                  orient=tk.HORIZONTAL, length=200).grid(row=1, column=1, padx=5)
        ttk.Label(ctrl, textvariable=self.it).grid(row=1, column=2)

        btnf = ttk.Frame(ctrl)
        btnf.grid(row=2, column=0, columnspan=3, pady=5)
        ttk.Button(btnf, text='Iniciar', command=self.start).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnf, text='Restablecer', command=self.reset).pack(side=tk.LEFT)

        self.txt = tk.Text(frm, height=4)
        self.txt.pack(fill=tk.X)

        viz = ttk.LabelFrame(frm, text='Visualización')
        viz.pack(fill=tk.BOTH, expand=1)

        fig = Figure(figsize=(6, 4))
        self.ax = fig.add_subplot(211)
        self.ax_err = fig.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(fig, viz)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def start(self):
        if self.running:
            self.running = False
            return
        self.model = PerceptronModel(n=50, lr=self.lr.get(),
                                     max_iter=self.it.get(), rng=10)
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def reset(self):
        self.running = False
        self.txt.delete(1.0, tk.END)
        self.ax.clear()
        self.ax_err.clear()
        self.canvas.draw()

    def _run(self):
        while self.running and self.model.running:
            self.model.step()
            self._update()
            time.sleep(0.1)
        self.running = False

    def _update(self):
        m = self.model
        # Limpiar
        self.ax.clear()
        self.ax_err.clear()
        # Puntos y frontera
        data = [a for a in m.schedule.agents if isinstance(a, DataPointAgent)]
        for a in data:
            mk = 'o' if a.label == -1 else '^'
            self.ax.scatter(a.x, a.y, c=a.color, marker=mk)
        xs, ys = m.perc.get_decision_boundary((-m.data_range, m.data_range))
        self.ax.plot(xs, ys, 'g-')
        self.ax.set_title(f'Época {m.perc.epoch}')
        self.ax.grid(True)
        # Error
        self.ax_err.plot(range(len(m.perc.errors)), m.perc.errors, 'r-')
        self.ax_err.set_xlabel('Época')
        self.ax_err.set_ylabel('Error')
        self.ax_err.grid(True)
        self.canvas.draw()
        # Texto
        err = m.perc.errors[-1] if m.perc.errors else 0
        self.txt.delete(1.0, tk.END)
        self.txt.insert(tk.END, f'Época: {m.perc.epoch}\nError: {err}\n')

if __name__ == '__main__':
    PerceptronUI()
