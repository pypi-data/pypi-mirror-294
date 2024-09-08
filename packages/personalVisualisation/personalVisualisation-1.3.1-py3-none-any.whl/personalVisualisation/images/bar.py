from . import get_logger
import matplotlib.pyplot as plt
import io
from custom_development_standardisation import *

def generate_bar_chart(data_labels,values,title,x_axis_label,y_axis_label):
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    # Create a bar chart
    plt.bar(data_labels, values, color='blue')

    # Add title and labels
    plt.title(title)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)

    # Display the chart
    plt.savefig('bar_chart.png', format='png')

    output = io.BytesIO()
    plt.savefig(output,format='png')
    output.seek(0)
    
    return generate_outcome_message("success",output.getvalue())



# Sample data
# binary = generate_bar_chart(["something",'nothing','hello'],[1,2,3],"random","something","nothing")
# with open('saved_bar_chart.png', 'wb') as file:
#     file.write(binary["output"])


