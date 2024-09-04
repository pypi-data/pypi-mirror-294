import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def extract(file_address, column_name, plot=False, *args, **kwargs):
    d=pd.read_excel(file_address)
    ndf=d.filter(items=[column_name])
    img_addr=kwargs.get('img_addr',None)
    img_name=kwargs.get('img_name',None)
    plot_title=kwargs.get('plot_title',None)
    x_name=kwargs.get('x_name',None)
    y_name=kwargs.get('y_name',None)
    if plot==True:
            yp1=np.array(ndf[column_name].tolist())
            plt.plot(yp1)
            plt.title(plot_title)
            plt.xlabel(x_name)
            plt.ylabel(y_name)

            fig=plt.gcf()
            plt.show()
            plt.draw()
            img_addr=img_addr+img_name
            fig.savefig(img_addr+'.jpg', dpi=100)
    return ndf


def hello():
     print("Hello, World!")