#!/usr/bin/env python3
"""Module to manage the user interface"""

import json
from pathlib import Path
import tkinter as tk
from lib.transform_canvas import TransformCanvas
from lib import widgets
from lib.utils import truncate_rounding
from lib.drawings import Chart
from lib.constants import GLYPHS, PLANETS

CYCLE_TEXTS = ['2-D Radix\nHorizon view\nOrigo: Tropos',
               '2-D Turned\nDerived houses\nRadix Quadrants']

DATA_DIR = Path('aqCHARTS/aq_temp')

def load_data():
    data = json.load(open(DATA_DIR / 'data.json'))
    angles = data['angles']
    return {"letters": [GLYPHS[p] for p in PLANETS] + ['MC', 'ASC'],
            "base_angles": angles,
            "chart_angles": angles,
            "truncated_angles": list(map(truncate_rounding, angles))}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ChartDraw')
        frame = tk.Frame(self)
        frame.pack()
        left_frame = tk.Frame(frame)
        left_frame.pack(side=tk.LEFT)
        right_frame = tk.Frame(frame)
        right_frame.pack(side=tk.RIGHT)

        self.data = load_data()

        top_bar = tk.Frame(left_frame, borderwidth=5)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        tl_text = tk.Label(top_bar,
                           text='Tropical Zodiac\nEqual Houses\nQuadrants')
        tl_text.pack(side=tk.LEFT)
        tr_text = tk.Label(top_bar, text='DRAW\nzh 2\nZET9')
        tr_text.pack(side=tk.RIGHT)

        canvas = TransformCanvas(left_frame, background="#1D1F21",
                                 width=512, height=512)
        canvas.pack(side=tk.TOP)
        self.chart = Chart(canvas)
        bottom_bar = tk.Frame(left_frame, borderwidth=5)
        bottom_bar.pack(side=tk.TOP, fill=tk.X)
        self.cycle_status = tk.StringVar(self, value=CYCLE_TEXTS[0])
        bl_text = tk.Label(bottom_bar, textvariable=self.cycle_status)
        bl_text.pack(side=tk.LEFT)

        reset_button = tk.Button(bottom_bar, text="Reset chart",
                                 command=self.reset_chart)
        reset_button.pack(side=tk.TOP)

        self.harmonic_frame = widgets.HarmonicSelection(
            right_frame,
            apply_command=self.harmonic,
            spinbox_command=self.turned_axes_frame_reset)
        self.harmonic_frame.pack(side=tk.TOP)
        self.turned_axes_frame = widgets.CycleSelection(
            right_frame,
            apply_command=self.turned,
            spinbox_command=self.harmonic_frame.reset)
        self.turned_axes_frame.pack(side=tk.TOP)

        self.tv = widgets.TreeviewPanel(right_frame, self.data)
        self.tv.pack(side=tk.TOP)

        self.focus_set()
        self.bind('<Key>', self.dispatch)

        self.chart.draw_chart(self.data['base_angles'])

    def dispatch(self, event):
        if event.char == '=':
            self.tv.toggle_column()
        elif event.char == '+':
            self.tv.scroll_up()
        elif event.char == 'h':
            self.harmonic()
        elif event.char == 't':
            self.turned()
        elif event.char == 'a':
            self.aspects()
        elif event.keysym == 'Escape':
            self.focus_set()
    
    def turned_axes_frame_reset(self):
        self.turned_axes_frame.reset()

    def reset_chart(self):
        self.harmonic_frame.reset()
        self.turned_axes_frame.reset()
        self.data['chart_angles'] = self.data['base_angles']
        self.chart.draw_chart(self.data['base_angles'])

    def harmonic(self):
        result = self.harmonic_frame.get()
        self.turned_axes_frame.reset()
        if not result:
            return
        options = {}
        if result != 1:
            options['axes_text'] = ['HAR', 'HAR']
        harmonic_angles = [(result * ang) % 360 for ang in self.data['base_angles']]
        self.data['chart_angles'] = harmonic_angles
        self.chart.draw_chart(harmonic_angles, **options)

    def turned(self):
        result = self.turned_axes_frame.get()
        self.harmonic_frame.reset()
        if result != 1:
            self.cycle_status.set(CYCLE_TEXTS[1])
            self.chart.draw_chart(self.data['base_angles'], cycle=result,
                                  axes_text=['Turned', 'Turned'])
        else:
            self.cycle_status.set(CYCLE_TEXTS[0])
            self.chart.draw_chart(self.data['base_angles'], cycle=result)

    def aspects(self):
        self.chart.aspects(self.data['chart_angles'])


if __name__ == '__main__':
    app = App()
    app.mainloop()
