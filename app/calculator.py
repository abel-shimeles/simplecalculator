import math
import tkinter as tk
from utils.get_settings import get_settings
from utils.split_strings import split_strings
from utils.add_to_history import add_to_history
from utils.read_history import read_history
from utils.clear_history import clear_history
from functools import partial


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x677")
        self.window.resizable(True, True)
        self.window.title("Calculator")

        original_width = 500
        original_height = 677
        min_width = int(original_width * 0.85)
        min_height = int(original_height * 0.85)

        self.window.wm_minsize(min_width, min_height)

        icon = tk.PhotoImage(file="favicon.png")
        self.window.iconphoto(True, icon)
        self.history = read_history()
        self.settings = get_settings()
        self.control_history = False

        self.total_expression = ""
        self.current_expression = "0"
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (3, 2),
            8: (3, 3),
            9: (3, 4),
            4: (4, 2),
            5: (4, 3),
            6: (4, 4),
            1: (5, 2),
            2: (5, 3),
            3: (5, 4),
            0: (6, 3),
            ".": (6, 2),
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # self.history_frame = self.create_history_frame()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()
        self.create_history_icon()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())

        for key in self.digits:
            self.window.bind(
                str(key), lambda event, digit=key: self.add_to_expression(digit)
            )

        for key in self.operations:
            self.window.bind(
                key, lambda event, operator=key: self.append_operator(operator)
            )

        self.window.bind("<BackSpace>", lambda event: self.backspace())
        self.window.bind("<parenleft>", lambda event: self.add_to_expression("("))
        self.window.bind("<parenright>", lambda event: self.add_to_expression(")"))
        self.window.bind("<plusminus>", lambda event: self.plus_minus())

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_backspace_button()
        self.create_parentheses_buttons()
        self.create_plus_minus_button()
        self.create_modular_button()
        self.create_change_button()
        self.create_ln_button()
        self.create_log_button()
        self.create_factorial_button()
        self.create_pi_button()
        self.create_sin_button()
        self.create_cos_button()
        self.create_tan_button()
        self.create_absolute_value_button()
        self.create_two_power_button()
        self.create_euler_button()
        self.create_euler_power_button()

    def create_display_labels(self):
        total_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg=self.settings["display_labels_color"],
            fg=self.settings["label_color"],
            padx=24,
            font=self.settings["small_font_style"],
        )
        total_label.pack(expand=True, fill="both")

        label = tk.Label(
            self.display_frame,
            text=self.current_expression,
            anchor=tk.E,
            bg=self.settings["display_labels_color"],
            fg=self.settings["label_color"],
            padx=24,
            font=self.settings["large_font_style"],
        )
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(
            self.window, height=221, bg=self.settings["display_labels_color"]
        )
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        if len(self.total_expression) < 60:
            if self.current_expression[0] == "0":
                self.current_expression = ""
                self.current_expression += str(value)
            else:
                self.current_expression += str(value)
            self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg=self.settings["digits_color"],
                fg=self.settings["label_color"],
                font=self.settings["digits_font_style"],
                borderwidth=0,
                command=lambda x=digit: self.add_to_expression(x),
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):

        if len(self.total_expression) <= 60:
            self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression, removed_operator = split_strings(
                self.total_expression
            )
            self.update_total_label()
            self.update_label()
        else:
            maximum = self.create_maximum_operations_label()

            return maximum

    def create_operator_buttons(self):
        i = 2
        for operator, symbol in self.operations.items():
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=self.settings["special_characters_color"],
                fg=self.settings["label_color"],
                font=self.settings["operators_font_style"],
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x),
            )
            button.grid(row=i, column=5, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = "0"
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="C",
            bg=self.settings["special_characters_color"],
            fg=self.settings["clear_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.clear,
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**2"))
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_square_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.square,
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def sqrt(self):
        try:
            if eval(self.current_expression) >= 0:
                self.current_expression = str(eval(f"{self.current_expression}**0.5"))
            else:
                self.current_expression = "Error"
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.sqrt,
        )
        button.grid(row=0, column=4, sticky=tk.NSEW)

    def evaluate(self):

        if not ("Error" in self.current_expression):
            self.total_expression += self.current_expression
            self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            add_to_history(self.total_expression, self.current_expression)
            self.history = read_history()
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="=",
            bg=self.settings["equals_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.evaluate,
        )
        button.grid(row=6, column=5, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")

        for x in range(6):
            frame.rowconfigure(x, weight=1)
        for y in range(1, 6):
            frame.columnconfigure(y, weight=1)

        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:12])

    def backspace(self):
        if (
            len(self.current_expression) > 1
            and self.current_expression != "0"
            and self.current_expression != "Error"
        ):
            self.current_expression = self.current_expression[:-1]
        elif (
            self.current_expression == "0"
            or len(self.current_expression) <= 1
            and self.current_expression != "Error"
        ):
            self.current_expression = "0"
        elif "Error" in self.current_expression:
            self.current_expression = "0"
            self.total_expression = ""
            self.update_total_label()
        self.update_label()

    def create_backspace_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="⌫",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.backspace,
        )
        button.grid(row=0, column=5, sticky=tk.NSEW)

    def create_parentheses_buttons(self):
        button_open = tk.Button(
            self.buttons_frame,
            text=")",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=lambda: self.add_to_expression(")"),
        )
        button_close = tk.Button(
            self.buttons_frame,
            text="(",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=lambda: self.add_to_expression("("),
        )
        button_open.grid(row=1, column=5, sticky=tk.NSEW)
        button_close.grid(row=1, column=4, sticky=tk.NSEW)

    def plus_minus(self):
        if self.current_expression != "0":
            if self.current_expression.startswith("-"):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = "-" + self.current_expression
        self.update_label()

    def create_plus_minus_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="+/-",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.plus_minus,
        )
        button.grid(row=1, column=2, sticky=tk.NSEW)

    def create_modular_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="mod",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=lambda: self.add_to_expression("%"),
        )
        button.grid(row=1, column=3, sticky=tk.NSEW)

    def create_change_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="⇌",
            bg=self.settings["digits_color"],
            fg=self.settings["label_color"],
            font=self.settings["digits_font_style"],
            borderwidth=0,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def sin(self):
        try:
            result = math.sin(math.radians(eval(self.current_expression)))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_sin_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="sin",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.sin,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def cos(self):
        try:
            result = math.cos(math.radians(eval(self.current_expression)))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_cos_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="cos",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.cos,
        )
        button.grid(row=1, column=1, sticky=tk.NSEW)

    def tan(self):
        try:
            if (
                eval(self.current_expression) % 90 == 0
                and eval(self.current_expression) % 180 != 0
                and eval(self.current_expression) != 0
            ):
                result = "Error"
            else:
                result = math.tan(math.radians(eval(self.current_expression)))

            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_tan_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="tan",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.tan,
        )
        button.grid(row=2, column=1, sticky=tk.NSEW)

    def pi(self):
        try:
            result = math.pi
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_pi_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="π",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.pi,
        )
        button.grid(row=6, column=4, sticky=tk.NSEW)

    def abs(self):
        try:
            result = abs(eval(self.current_expression))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_absolute_value_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="|x|",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.abs,
        )
        button.grid(row=3, column=1, sticky=tk.NSEW)

    def two_power(self):
        try:
            self.current_expression = str(eval(f"2**{self.current_expression}"))
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_two_power_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="2\u02E3",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.two_power,
        )
        button.grid(row=4, column=1, sticky=tk.NSEW)

    def euler_power(self):
        try:
            result = math.exp(eval(self.current_expression))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_euler_power_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="e\u02E3",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.euler_power,
        )
        button.grid(row=5, column=1, sticky=tk.NSEW)

    def e(self):
        try:
            result = math.e
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_euler_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="e",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.e,
        )
        button.grid(row=6, column=1, sticky=tk.NSEW)

    def ln(self):
        try:
            result = math.log(eval(self.current_expression))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_ln_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="ln",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.ln,
        )
        button.grid(row=2, column=2, sticky=tk.NSEW)

    def log(self):
        try:
            result = math.log(eval(self.current_expression), 10)
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_log_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="log",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.log,
        )
        button.grid(row=2, column=3, sticky=tk.NSEW)

    def factorial(self):
        try:
            result = math.factorial(eval(self.current_expression))
            self.current_expression = str(result)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_factorial_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x!",
            bg=self.settings["special_characters_color"],
            fg=self.settings["label_color"],
            font=self.settings["default_font_style"],
            borderwidth=0,
            command=self.factorial,
        )
        button.grid(row=2, column=4, sticky=tk.NSEW)

    def create_maximum_operations_label(self):
        label = tk.Label(
            self.buttons_frame,
            text="maximum operations",
            bg="gray",
            fg="white",
            font=self.settings["small_font_style"],
            borderwidth=10,
        )
        label.grid(row=4, column=2, columnspan=3)

        label.after(2000, label.destroy)

    def create_history_frame(self):

        frame = tk.Frame(self.buttons_frame, background="black")
        frame.grid(row=0, column=1, rowspan=7, columnspan=5, sticky=tk.NSEW)
        return frame

    def create_history_buttons(self, flag):

        if flag == True:
            history_frame = self.create_history_frame()
            self.history_frame = history_frame

            row = 0

            if self.history != "No History":
                for total_expression, current_expression in self.history.items():
                    button = tk.Button(
                        history_frame,
                        text=f"operation: {total_expression}\t result: {current_expression}",
                        bg="black",
                        fg=self.settings["label_color"],
                        font=self.settings["default_font_style"],
                        borderwidth=0,
                        command=partial(
                            self.change_history_values,
                            total_expression,
                            current_expression,
                        ),
                    )

                    button.grid(
                        row=row,
                        column=1,
                        columnspan=5,
                        sticky=tk.NSEW,
                    )
                    row += 3

                    clear_history_icon = tk.PhotoImage(file="clear_history_icon.png")

                    clear_history_button = tk.Button(
                        self.history_frame,
                        image=clear_history_icon,
                        command=self.clear_history_values,
                        bg="black",
                        fg="gray",
                        borderwidth=0,
                    )
                    clear_history_button.image = clear_history_icon

                    button_width = clear_history_icon.width()
                    button_height = clear_history_icon.height()
                    window_width = self.history_frame.winfo_width()
                    window_height = self.history_frame.winfo_height()

                    button_x = window_width - button_width - 20
                    button_y = window_height - button_height - 20

                    clear_history_button.place(x=375, y=450)
                    self.clear_history_button = clear_history_button
                    self.history_frame = history_frame
            else:
                frame = tk.Frame(history_frame, bg="black")
                frame.pack(expand=True, fill="both")
                label = tk.Label(
                    frame,
                    text="No History",
                    fg="white",
                    bg="black",
                    font=self.settings["default_font_style"],
                )
                label.pack()
                label.place(x=175, y=10)


                clear_history_icon = tk.PhotoImage(file="clear_history_icon.png")

                clear_history_button = tk.Button(
                    self.history_frame,
                    image=clear_history_icon,
                    command=self.clear_history_values,
                    bg="black",
                    fg="gray",
                    borderwidth=0,
                )
                clear_history_button.image = clear_history_icon

                button_width = clear_history_icon.width()
                button_height = clear_history_icon.height()
                window_width = self.history_frame.winfo_width()
                window_height = self.history_frame.winfo_height()

                button_x = window_width - button_width - 20
                button_y = window_height - button_height - 20

                clear_history_button.place(x=350, y=450)
                self.clear_history_button = clear_history_button
                self.history_frame = history_frame
                self.clear_history_button.destroy()

        else:
            self.history_frame.destroy()
            self.clear_history_button.destroy()

    def change_history_values(self, total, current):
        self.total_expression = total
        self.current_expression = current
        self.update_label()
        self.update_total_label()

    def clear_history_values(self):
        clear_history()
        self.history = read_history()
        self.control_history = not self.control_history
        self.clear_history_button.destroy()
        self.history_frame.destroy()

    def control_history_frame(self):
        self.control_history = not self.control_history
        self.create_history_buttons(self.control_history)

    def create_history_icon(self):
        history_icon = tk.PhotoImage(file="history_icon.png")

        history_button = tk.Button(
            self.window,
            image=history_icon,
            command=self.control_history_frame,
            bg=self.settings["display_labels_color"],
            borderwidth=0,
        )
        history_button.image = history_icon
        history_button.place(x=20, y=20)

    def run(self):
        self.window.mainloop()
