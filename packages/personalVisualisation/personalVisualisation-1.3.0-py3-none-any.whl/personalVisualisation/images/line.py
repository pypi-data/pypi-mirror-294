from . import logger
import matplotlib.pyplot as plt
import pandas as pd
from custom_development_standardisation import *
from datetime import datetime, timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from PIL import Image



def generate_line_chart(x, y):
    try:
        logger.store_log()
    except Exception as e:
        None

    
    try:
        data = pd.DataFrame({
            'x': x,
            'y': y
        })

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['x'], data['y'], linestyle='-')

        # Set the title and labels
        ax.set_title('Line Chart with Date on X-Axis and Integer Range on Y-Axis')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # Rotate date labels for better readability
        plt.xticks(rotation=45)

        # Display the grid
        ax.grid(True)
        plt.tight_layout()

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        FigureCanvas(fig).print_png(buf)
        buf.seek(0)

        # Load image from binary data
        # image = Image.open(buf)

        # Close the plot to free memory
        plt.close(fig)

        # Return the PIL Image object
        return generate_outcome_message("success",buf.getvalue())

    except:
        return generate_outcome_message("error","something went wrong with generate line chart..",the_type="custom")
    # Create a pandas DataFrame
    


# # Example usage
# x = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(10)]
# y = range(10)
# image = generate_line_chart(x, y)

# # You can save the image to a file if needed
# # image.save('line_chart.png')

# # Example of using the image, e.g., displaying it
# image.show()