from . import logger

from custom_development_standardisation import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

# import matplotlib
# matplotlib.use('Agg')

def generate_pie_chart_image_data(data):
    
    try:
        logger.store_log()
    except Exception as e:
        None

    if not isinstance(data, dict):
        return generate_outcome_message(
            "error",
            "Parameter is not an object",
            the_type="custom"
        )

    for key, value in data.items():
        if not isinstance(value, (int, float)):
            return generate_outcome_message(
                "error",
                f"The key '{key}' does not have a number value.",
                the_type="custom"
            )
    
    # labels = ['A', 'B', 'C', 'D']
    # sizes = [15, 30, 45, 10]
    labels = []
    sizes = []
    total = 0

    for i,j in data.items():
        total += j
        labels.append(i)
        sizes.append(j)
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    wedgeprops = {'linewidth': 1, 'edgecolor': 'black'}
    _, texts, autotexts = ax.pie(sizes, labels=labels, autopct=custom_autopct, wedgeprops=wedgeprops)

    ax.axis('equal')
    fig.tight_layout()

    # Generate the pie chart
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    # print(output.getvalue())
    
    # Clear memory
    plt.close(fig)

    return generate_outcome_message("success",output.getvalue())






def custom_autopct(pct):
    
    # Customize the autopct logic here
    if pct >= 5:
        return f'{pct:.1f}%'
    else:
        return ''
    


# from personalDatabase.foundation import *
# x = foundation()
# outcome = x.initialise("logging_data","marcus")
# print(outcome)
# outcome = x.retrieve("SELECT utility, COUNT(*) as utility_count FROM usage_data GROUP BY utility order by utility_count asc")



# obj = {}
# for i in outcome["output"]:
#     obj[i[0]] = i[1]

# print(obj)

# generate_pie_chart(obj)
