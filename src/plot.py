'''   @file                            plot.py
   @brief                              Plots closed loop controller response.
   @details                            Plots closed loop controller response. Utilizes the plotResponse and initTest functions.                                       
   @author                             Jason Davis
   @author                             Conor Fraser
   @author                             Adam Westfall
   @copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
   @date                               Feb 13, 2023
'''


from matplotlib import pyplot as p

def plotResponse(csv_filename):
    '''!  @brief                              Plots the response of the test results.
       @details                               Plots the response of the test results. Sets x and y axis labels.
                                              Sets the title of the plot. The x and y data start as empty lists and
                                              get appended as data is collected.
       @param list                            Parses in a list of parameters to hit the low Kp, high Kp, and best performance targets.
       @param gain                            Parses in the Kp.    
       @param target_pos                      Parses in the target motor position.
       @param test_num                        Parses in which test is running.
    '''
    p.title("Theta vs Time")
    p.xlabel("Time, seconds")
    p.ylabel("Theta, encoder_ticks")
    p.grid(True)
    x = []
    y = []
    with open(csv_filename, 'r') as csv_file:
        for line in csv_file:
            i = line.strip().split(' ')
            if len(i) == 2:
                x.append(int(i[0]))
                y.append(int(i[1]))
    p.plot(x,y)
    p.show()    

if __name__ == "__main__":
    csv_filename = "data.csv"
    plotResponse(csv_filename)
