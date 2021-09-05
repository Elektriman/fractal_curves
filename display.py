# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 11:57:15 2021

@author: Julien
"""

#  _____                            _       
# |_   _|                          | |      
#   | |  _ __ ___  _ __   ___  _ __| |_ ___ 
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |                       
#                 |_|

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

import sierpinski_triangle as ST
import dragon_curve as DC
import Levi_curve as LC


#  ______                _   _                 
# |  ____|              | | (_)                
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                      
def complex_to_plot(T):
    '''
    transforms a list of complex numbers and returns two lists of x and y coordinates.
    x represents the real componant and y represents the imaginary componant for each point

    Parameters
    ----------
    T : list[complex]
        a list of complex numbers you want to display

    Returns
    -------
    X, Y
        the real (X) and imaginary (Y) componants of each point
    '''
    return [el.real for el in T], [el.imag for el in T]

def plot_to_complex(A,B):
    '''
    returns the list of complex numbers caracterized by their real and imaginary componants.
    A and B must be of equal dimentions.

    Parameters
    ----------
    A : list[float]
        real componants.
    B : list[float]
        complex componants.

    Returns
    -------
    list[complex]
        a list of complex numbers.

    '''
    return [complex(a,b) for a,b in zip(A,B)]

def fixed_display(construction_function, order, lim, stroke_width=1, ax=None, plot=True, save=False):
    '''
    displays a fractal curve without animation

    Parameters
    ----------
    construction_function : string
        The string of the construction function for a given fractal.
        The nomenclature for such string should be the name of the curve in lower case and snake case.
    order : int
        The number of steps of the construction algorithm that will be displayed.
    lim : ((float, float), (float, float))
        The tuple ((min_x, max_x),(min_y, max_y)) used for a better view while plotting.
    ax : matplotlib.axes.Axes
        The axis on which the curve must be plotted. The default is None.
        If not given, a new figure will be initialised.
    stroke_width : float, optional
        The width of the stroke for plotting. The default is 1.
    plot : boolean, optional
        Wether to plot the result or not. The default is True.
    save : boolean, optional
        Wether to save the result as a csv file of not. The default is False.
    '''
    
    if ax == None :
        fig, ax = plt.subplots(figsize=(10,7))
    
    #using the imported library for constructing the points of the curve
    E = construction_function(order)
    E_real = [el.real for el in E]
    E_imag = [el.imag for el in E]
    
    #plotting the data
    if plot :
        ax.plot(E_real, E_imag, lw=stroke_width/np.log(len(E)))
        ax.axis('equal')
        xlim, ylim = lim
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
    
    #saving the data as csv
    if save :
        try :
            #making a new directory named after the curve
            os.mkdir(os.path.join(os.path.dirname(__file__), f"{construction_function.__name__}"))
        except Exception as e :
            #an exception should be raised when the directory already exists.
            #the exception is not raised because it would stop the program
            pass
        
        #saving csv files named "{curve_name}_{order}.csv"
        #there is on csv for each order of the fractal curve computation
        with open(f"{construction_function.__name__}\{construction_function.__name__}_{order}.csv", "w") as f :
            W = csv.writer(f, delimiter=',', lineterminator='\r') #using csv library to save as csv.
            '''
            some problems were encountered while saving in csv formatting. Every other row was empty because of the 
            redundancy of '\r' character. The "lineterminator='\r'" fixed it following this post :
            https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
            '''
            Coords = [[E_real[i],E_imag[i]] for i in range(len(E))]
            W.writerows(Coords)

def animated_display(partial_function, max_order, lim, stroke_width=1):
    '''
    Displays an animation of the fractal curve construction.

    Parameters
    ----------
    partial_function : string
        the function that makes the fractal construction algorithm go one order further.
    max_order : int
        the maximal order to display.
    lim : ((float, float), (float, float))
        The tuple ((min_x, max_x),(min_y, max_y)) used for a better view while plotting.
    '''
    from matplotlib import animation
    
    fig, ax = plt.subplots(figsize=(10,7))
    
    x_lim, y_lim = lim
    #plotting two points to fix the limits of the plot
    F, = ax.plot([x_lim[0], x_lim[1]],[y_lim[0], y_lim[1]])
    #doing it via "ax.set_xlim()" will not work and I can't explain why.
    
    #the order value that needs to be global to avoid it being reset at each pass throught the animation function
    global order
    order = 0
    #I could have passed it as a parameter for the animation function. It is a more proper way to do it
    #but also harder. It wasn't worth the effort.
    
    def init():
        '''
        Function called once at the start of the animation

        Returns
        -------
        F : list[matplotlib.lines.Line2D]
            The object returned by the "plot()" method. It is used as parameter for the animation process.
            https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation
        '''
        F.set_data(complex_to_plot([complex(0,0), complex(1,0)]))
        F.set_linewidth(3)
        return F,
    
    def animate(i, F):
        '''
        Function called in loops for the animation
        
        Parameters
        ----------
        F : list[matplotlib.lines.Line2D]
            The object returned by the "plot()" method. It is used for the animation process.
            https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation

        Returns
        -------
        F : list[matplotlib.lines.Line2D]
            The object returned by the "plot()" method. It is used as parameter for the animation process.
            https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation
        '''
        #recovering the order and the stroke width
        global order
        
        #changing the data to plot
        F.set_data(complex_to_plot(partial_function(plot_to_complex(F.get_xdata(), F.get_ydata()))))
        F.set_linewidth(3/np.log(len(F.get_xdata()))) #making the stroke thinner as the number of edges goes up
        
        order+=1
        if order==max_order : #if we got to the max order
            #reseting the whole plot
            order = 0
            F.set_data(complex_to_plot([complex(0,0), complex(1,0)]))
            F.set_linewidth(3/np.log(len(F.get_xdata())))
        
        ax.axis('equal')
        return F,
    
    #the animation process happens here
    ani = animation.FuncAnimation(fig, animate, fargs=(F,), init_func=init, blit=True, interval=1500)
    '''
    fig : matplotlib.figure
        The figure on which you want your animation.
    animate : function
        The function called in loops to make the animation progress
    fargs : tuple
        The arguments to pass throught one call of the animation function to another.
        Plottable objects are preffered, and they help the animation performances.
    init_func : function
        The function called once at the start of the animation process. As the "animate" function,
        the return values help the performances and should be plottable objects.
    blit : boolean
        Use the feature of returning modified objects in the animate function to boost the animation
        performances.
    interval : int
        the number of miliseconds between two calls of the "animate" function.
    
    for more info :
        https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation
    '''

#  _            _       
# | |          | |      
# | |_ ___  ___| |_ ___ 
# | __/ _ \/ __| __/ __|
# | ||  __/\__ \ |_\__ \
#  \__\___||___/\__|___/

if __name__ == '__main__' :
    N = 18 #max number of iterations for dragon and Levy curve
    T = 12 #max number of itertions for the sierpinski triangle
    
    #limits for each curve plot
    DC_LIMITS = (DC.X_LIMITS, DC.Y_LIMITS)
    LC_LIMITS = (LC.X_LIMITS, LC.Y_LIMITS)
    ST_LIMITS = (ST.X_LIMITS, ST.Y_LIMITS)
    
    '''fixed displays'''
    # fixed_display(DC.dragon_curve, N, DC_LIMITS, 2)
    # fixed_display(LC.Levi_curve, N, LC_LIMITS, 3)
    # fixed_display(ST.sierpinski_triangle, T, ST_LIMITS, 2)
    
    '''collection of fixed displays in the same figure'''
    # fig, ax = plt.subplots(2,2, figsize=(10,7))
    # fixed_display(DC.dragon_curve, N, DC_LIMITS, 2, ax[0,0])
    # fixed_display(LC.Levi_curve, N, LC_LIMITS, 2, ax[0,1])
    # fixed_display(ST.sierpinski_triangle, T, ST_LIMITS, 2, ax[1,0])
    
    '''animated displays (run only one at a time)'''
    # animated_display(DC.partial_dragon_curve, N, DC_LIMITS)
    # animated_display(LC.partial_Levi_curve, N, LC_LIMITS)
    # animated_display(ST.partial_sierpinski_triangle, T, ST_LIMITS)
    
    plt.show()