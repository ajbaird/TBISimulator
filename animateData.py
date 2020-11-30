#----------------------------------------------------------#
# This file will take command line inputs and create an animated plot of your data
# for a given x and y value
#----------------------------------------------------------#



from matplotlib import dates as mdate
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import sys, getopt 
import os

def fileData(argv):
   inputfile = ''
   outputfile = ''
   xcolumn = ''
   ycolumn = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:x:y:",["ifile=","ofile=", "xcol=, ycol="])
   except getopt.GetoptError:
      print ('USAGE: animateData.py -i <inputfile> -o <outputfile> -x <xcolumn>, -y <ycolumn>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('USAGE: animateData.py -i <inputfile> -o <outputfile> -x <xcolumn>, -y <ycolumn>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-x", "--xcol"):
         xcolumn = arg
      elif opt in ("-y", "--ycol"):
         ycolumn = arg

   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)   
   print ('x column name is ', xcolumn)
   print ('y column name is ', ycolumn)


   return inputfile, outputfile, xcolumn, ycolumn

def checkPath(inputfile, outputfile):
    absolutDirPath = os.path.abspath(os.path.dirname(__file__))
    absPathInput = os.path.abspath(inputfile)
    absPathOuput = os.path.abspath(outputfile)
    inputDirPath = os.path.join(absolutDirPath, absPathInput)
    ouputDirPath = os.path.join(absolutDirPath, absPathOuput)

    if os.path.isfile(inputDirPath):
        print('Input file found in: ', inputDirPath)
    else:
        print('Input file: ', inputDirPath,  'does not exist')
        sys.exit()
        
    print('output file will be saved in: ', ouputDirPath)


def animate(i, xcol, ycol):
    ax1.clear()
    ax1.plot(x[:i], y[:i])
    #ax1.set_xticks(ax1.get_xticks()[::10])
    #ax1.legend(loc = 'upper left')
    ax1.set_xlim([x.iloc[0],
                  x.iloc[-1]])
    ax1.set_ylim([y.iloc[0], y.iloc[-1]*1.1])

    ax1.set_ylabel(ycol)
    ax1.set_xlabel(xcol)



    #ax1.xaxis.set_major_locator(mdate.DayLocator(interval = 5))
    #ax1.xaxis.set_major_formatter(mdate.DateFormatter('%d-%m-%Y'))

def loadData(inputfile, ouputfile, xcol, ycol):
    print("\n checking if x and y values are present in the data")
    df = pd.read_csv(inputfile)
    print("\n headers of your data are: \n")
    print(list(df.columns.values.tolist()))

    if not xcol in df.columns:
        print("\n", xcol, " is not present in the data, please confirm spelling")
        sys.exit()

    if not ycol in df.columns:
        print("\n", ycol, " is not present in the data, please confirm spelling")
        sys.exit()

    outputDir = os.path.split(os.path.abspath(ouputfile))
    if not os.path.exists(outputDir[0]):
        print("\n  Output directory does not exist, creating it: ")
        os.makedirs(outputDir[0])
    else:
       print("Directory exits, continuing \n")

    x = df[xcol]
    y = df[ycol]

    return x, y

def formatGraph():
   plt.style.use('seaborn-white')

   plt.rcParams['font.family'] = 'serif'
   plt.rcParams['font.serif'] = 'Ubuntu'
   plt.rcParams['font.monospace'] = 'Ubuntu Mono'
   plt.rcParams['font.size'] = 10
   plt.rcParams['axes.labelsize'] = 10
   plt.rcParams['axes.labelweight'] = 'bold'
   plt.rcParams['axes.titlesize'] = 10
   plt.rcParams['xtick.labelsize'] = 8
   plt.rcParams['ytick.labelsize'] = 8
   plt.rcParams['legend.fontsize'] = 10
   plt.rcParams['figure.titlesize'] = 12  
   plt.locator_params(nbins=10)

   # Set an aspect ratio
   width, height = plt.figaspect(1.68)
   fig = plt.figure(figsize=(height, width), dpi=400)

   return fig




if __name__ == "__main__":

    # Check and process the command line arguments  
    inputfile, outputfile, xcolumn, ycolumn = fileData(sys.argv[1:])

    # Confirm that the paths exist and create output directory, if needed
    checkPath(inputfile, outputfile)

    # Load in the data, confirm headers exist and hand back the arrays for data
    x, y = loadData(inputfile, outputfile, xcolumn, ycolumn)

    fig = formatGraph()
    ax1 = fig.add_subplot(111)


    ani = animation.FuncAnimation(fig, animate, interval = 100, save_count= x.size, fargs=(xcolumn, ycolumn,))
    print(outputfile)
    ani.save('./output/test.mp4')
    #plt.show()
