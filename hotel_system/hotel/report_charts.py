import base64
import io

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt


def make_line_chart(labels, values, y_axis_label, color='#2563eb'):
    figure, axes = plt.subplots(figsize=(7, 2.8), dpi=150)
    axes.plot(labels, values, color=color, linewidth=2, marker='o', markersize=4)
    axes.fill_between(labels, values, color=color, alpha=0.08)
    axes.set_ylabel(y_axis_label, fontsize=9)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.tick_params(labelsize=8)
    axes.grid(axis='y', linestyle='--', alpha=0.3)
    figure.tight_layout()

    buffer = io.BytesIO()
    figure.savefig(buffer, format='png')
    plt.close(figure)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')
