from . import get_logger
import matplotlib.pyplot as plt
import pandas as pd
from custom_development_standardisation import *
from datetime import datetime, timedelta

import io
from PIL import Image



def popup_line_chart(title,obj):
    
    try:
        get_logger().store_log()
    except Exception as e:
        None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    collection = []
    for name,data in obj.items():
        
        final, = ax.plot(data['x'], data['y'], linestyle='-',label=name)
        plt.annotate(name,xy=(data['x'][60],data['y'][60]))
        collection.append(final)

    # Create a figure and axis

    # Set the title and labels
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # fig_legend, ax_legend = plt.subplots()
    # ax_legend.legend(handles=collection, loc='center', fontsize='small')
    # ax_legend.axis('off')  # Hide the axes
    # fig_legend.canvas.draw()  # Draw the canvas to create the legend

    # Display the grid
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    

# generate_line_chart([1,2,3,4,],[1,2,3,4,5,])

