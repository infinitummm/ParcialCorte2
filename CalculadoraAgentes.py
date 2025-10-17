import random
import re
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import operator

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class Message:
    def __init__(self, sender_id, receiver_id, msg_type, data, timestamp=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.msg_type = msg_type
        self.data = data
        self.timestamp = timestamp or time.time()
        self.processed = False


class MessageQueue:
    def __init__(self):
        self.queue = deque()
        self.history = []

    def send_message(self, message):
        self.queue.append(message)
        self.history.append(message)

    def get_messages_for_agent(self, agent_id):
        messages = []
        remaining = deque()
        while self.queue:
            msg = self.queue.popleft()
            if msg.receiver_id == agent_id and not msg.processed:
                messages.append(msg)
                msg.processed = True
            else:
                remaining.append(msg)
        self.queue = remaining
        return messages


class IOAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.current_expression = ""
        self.result = None
        self.status = "idle"

    def set_expression(self, expression):
        self.current_expression = expression
        self.result = None
        self.status = "processing"
        msg = Message(self.unique_id, 1, "parse_expression",
                     {"expression": expression})
        self.model.message_queue.send_message(msg)

    def step(self):
        messages = self.model.message_queue.get_messages_for_agent(self.unique_id)
        for msg in messages:
            if msg.msg_type == "final_result":
                self.result = msg.data["result"]
                self.status = "completed"


class ParserAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Cambiado '**' por '^'
        self.precedence = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
        self.pending_operations = []
        self.operation_results = {}

    def tokenize(self, expression):
        # Reconoce '^' en lugar de '**'
        tokens = re.findall(r'\d*\.?\d+|[+\-*/^()]', expression.replace(' ', ''))
        return tokens

    def infix_to_postfix(self, tokens):
        output = []
        stack = []
        for token in tokens:
            if re.match(r'\d*\.?\d+', token):
                output.append(float(token))
            elif token in self.precedence:
                while (stack and stack[-1] != '(' and
                       stack[-1] in self.precedence and
                       self.precedence[stack[-1]] >= self.precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
                    stack.pop()
        while stack:
            output.append(stack.pop())
        return output

    def step(self):
        messages = self.model.message_queue.get_messages_for_agent(self.unique_id)
        for msg in messages:
            if msg.msg_type == "parse_expression":
                expr = msg.data["expression"]
                self.process_expression(expr)
            elif msg.msg_type == "operation_result":
                op_id = msg.data["operation_id"]
                result = msg.data["result"]
                self.operation_results[op_id] = result
                self.check_completion()

    def process_expression(self, expression):
        try:
            tokens = self.tokenize(expression)
            postfix = self.infix_to_postfix(tokens)
            self.evaluate_postfix(postfix)
        except Exception as e:
            self.model.message_queue.send_message(
                Message(self.unique_id, 0, "final_result",
                        {"result": f"Error: {e}"}))

    def evaluate_postfix(self, postfix):
        stack = []
        operation_counter = 0
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Expresión inválida")
                b = stack.pop()
                a = stack.pop()
                operation_id = f"op_{operation_counter}"
                operation_counter += 1
                agent_id = self.get_agent_for_operation(token)
                self.model.message_queue.send_message(
                    Message(self.unique_id, agent_id, "perform_operation",
                            {"operation_id": operation_id,
                             "operator": token,
                             "operand1": a,
                             "operand2": b}))
                self.pending_operations.append(operation_id)
                stack.append(operation_id)
        self.final_result_placeholder = stack[0] if stack else None

    def get_agent_for_operation(self, operator):

        mapping = {'+': 2, '-': 3, '*': 4, '/': 5, '^': 6}
        return mapping.get(operator, 2)

    def check_completion(self):
        if not self.pending_operations:
            return
        if all(op_id in self.operation_results
               for op_id in self.pending_operations):
            final = self.operation_results[self.pending_operations[-1]]
            self.model.message_queue.send_message(
                Message(self.unique_id, 0, "final_result",
                        {"result": final}))
            self.pending_operations.clear()
            self.operation_results.clear()


class OperationAgent(Agent):
    def __init__(self, unique_id, model, operation_name, operation_func):
        super().__init__(unique_id, model)
        self.operation_name = operation_name
        self.operation_func = operation_func
        self.operations_performed = 0

    def step(self):
        messages = self.model.message_queue.get_messages_for_agent(self.unique_id)
        for msg in messages:
            if msg.msg_type == "perform_operation":
                self.perform_operation(msg.data)

    def perform_operation(self, data):
        a = data["operand1"]
        b = data["operand2"]
        oid = data["operation_id"]
        try:
            result = self.operation_func(a, b)
        except:
            result = float('inf')
        self.operations_performed += 1
        self.model.message_queue.send_message(
            Message(self.unique_id, 1, "operation_result",
                    {"operation_id": oid, "result": result}))


class CalculatorModel(Model):
    def __init__(self):
        super().__init__()
        self.message_queue = MessageQueue()
        self.schedule = RandomActivation(self)
        self.io_agent = IOAgent(0, self)
        self.parser_agent = ParserAgent(1, self)
        self.schedule.add(self.io_agent)
        self.schedule.add(self.parser_agent)
        self.schedule.add(OperationAgent(2, self, "Suma", operator.add))
        self.schedule.add(OperationAgent(3, self, "Resta", operator.sub))
        self.schedule.add(OperationAgent(4, self, "Multiplicación", operator.mul))
        self.schedule.add(OperationAgent(5, self, "División",
                                          lambda a, b: a / b if b != 0 else float('inf')))
        self.schedule.add(OperationAgent(6, self, "Potencia", operator.pow))

    def calculate_expression(self, expression):
        self.io_agent.set_expression(expression)
        while self.io_agent.status == "processing":
            self.step()
        return self.io_agent.result

    def step(self):
        self.schedule.step()


class CalculatorUI:
    def __init__(self):
        self.model = CalculatorModel()
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Calculadora Basada en Agentes ")
        self.root.geometry("1200x800")

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        input_frame = ttk.LabelFrame(main_frame, text="Entrada de Expresión")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Expresión matemática:")\
            .grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.expression_var = tk.StringVar(value="2 ^ 3 ")
        ttk.Entry(input_frame, textvariable=self.expression_var, width=30)\
            .grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="Calcular", command=self.calculate)\
            .grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(input_frame, text="Limpiar", command=self.clear)\
            .grid(row=0, column=3, padx=5, pady=5)

        result_frame = ttk.LabelFrame(main_frame, text="Resultado")
        result_frame.pack(fill=tk.X, pady=(0, 10))

        self.result_var = tk.StringVar(
            value="Ingrese una expresión y presione Calcular")
        ttk.Label(result_frame, textvariable=self.result_var,
                  font=('Arial', 12, 'bold')).pack(pady=10)

        comm_frame = ttk.LabelFrame(main_frame,
                                    text="Comunicación entre Agentes")
        comm_frame.pack(fill=tk.BOTH, expand=True)

        self.comm_text = scrolledtext.ScrolledText(comm_frame,
                                                   height=15, wrap=tk.WORD)
        self.comm_text.pack(fill=tk.BOTH, expand=True,
                            padx=5, pady=5)

        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.stats_var = tk.StringVar(
            value="Mensajes: 0 | Operaciones: 0")
        ttk.Label(stats_frame, textvariable=self.stats_var).pack(
            pady=5)

    def calculate(self):
        expr = self.expression_var.get().strip()
        if not expr:
            return
        self.comm_text.delete(1.0, tk.END)
        self.model = CalculatorModel()
        self.comm_text.insert(tk.END, f"Iniciando cálculo: {expr}\n")
        self.comm_text.insert(tk.END, "=" * 50 + "\n")
        result = self.model.calculate_expression(expr)
        self.result_var.set(f"{expr} = {result}"
                            if result is not None else
                            "Error en el cálculo")
        self.display_agent_communication()
        self.update_statistics()

    def clear(self):
        self.expression_var.set("")
        self.result_var.set(
            "Ingrese una expresión y presione Calcular")
        self.comm_text.delete(1.0, tk.END)
        self.stats_var.set("Mensajes: 0 | Operaciones: 0")

    def display_agent_communication(self):
        names = {0: "IOAgent", 1: "ParserAgent",
                 2: "SumAgent", 3: "SubAgent",
                 4: "MulAgent", 5: "DivAgent",
                 6: "PowAgent"}
        for i, msg in enumerate(self.model.message_queue.history, 1):
            s = names.get(msg.sender_id, str(msg.sender_id))
            r = names.get(msg.receiver_id, str(msg.receiver_id))
            self.comm_text.insert(tk.END,
                                 f"{i:2d}. {s} → {r}\n")
            self.comm_text.insert(tk.END,
                                 f"    Tipo: {msg.msg_type}\n")
            if msg.msg_type == "perform_operation":
                d = msg.data
                self.comm_text.insert(
                    tk.END,
                    f"    Operación: {d['operand1']} {d['operator']} {d['operand2']}\n")
            elif msg.msg_type in ("operation_result", "final_result"):
                self.comm_text.insert(
                    tk.END,
                    f"    Resultado: {msg.data['result']}\n")
            self.comm_text.insert(tk.END, "\n")
        self.comm_text.see(tk.END)

    def update_statistics(self):
        total_messages = len(self.model.message_queue.history)
        total_ops = sum(a.operations_performed
                        for a in [self.model.sum_agent,
                                  self.model.sub_agent,
                                  self.model.mul_agent,
                                  self.model.div_agent,
                                  self.model.pow_agent])
        self.stats_var.set(
            f"Mensajes enviados: {total_messages} | "
            f"Operaciones realizadas: {total_ops}")

    def run(self):
        self.root.mainloop()


def main():
    print("CALCULADORA BASADA EN AGENTES CON MESA")
    print("=" * 50)
    print("Mesa Framework 0.8.9 compatible")
    print("Inicializando aplicación...")
    try:
        app = CalculatorUI()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
