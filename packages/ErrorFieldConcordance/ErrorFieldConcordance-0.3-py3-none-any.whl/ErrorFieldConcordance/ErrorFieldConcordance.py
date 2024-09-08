# -*- coding: utf-8 -*-
"""
@author: Joe Rinehart
@contributors: Bernd Saugel
     Sean Coekelenbergh
     Ishita Srivastava
     Brandon Woo


"""
import numpy as np
import math
from matplotlib import pyplot as plt


def ErrorFieldConcordance(X,Y,plot_TF=False,graph_label="",
                          XMeasName="ΔX",
                          YMeasName="ΔY"):

    if (len(X) != len(Y)):
        print ("ErrorFieldConcordance: Reference and Test values must have" +\
               " the same number of observations.")
        return (0)
    if (len(X)<2):
        print ("ErrorFieldConcordance: Must have at least two observations per group")

    # Calculate changes
    DX = []
    DY = []
    for i in range(1,len(X)):
        DX.append(X[i] - X[i-1])
        DY.append(Y[i] - Y[i-1])

    plotcols = []

    TotalWeight = 0
    TotalScore = 0

    for i in range(len(DX)):
        # Point weight is the distance from the plotted point
        # to the origin (0,0).  This is the hypotenuse of the triangle
        # formed by sides of the lengths DX and DY.
        Hypot = np.hypot(DX[i],DY[i])
        # Calculate the Angle (a) that a line from the origin makes to
        # this point.  Sin (theta) = opp/hypot
        Angle = np.arctan((DY[i])/DX[i])
        Angle = math.degrees(Angle)
        # 'Score' the Agreement: angle <15 full credit (1 pt)
        #                        angle >75 full negative credit (-1 pt)
        #                        graded between 15 & 75
        # First Correct the angle - perfect is 45 degree line
        Angle -= 45
        if (Angle < -90):
            Angle += 180
        # Now calculate the score based on the angle
        Score = 0
        if (abs(Angle) <= 15):
            Score = 1
            # Graph color
            plotcols.append("blue")
        elif (abs(Angle) >= 75):
            Score = -1
            # Graph Color
            plotcols.append("red")
        else:
            # Yellow color is (1.0, 0.84, 0)
            Score = 1 - (2*(abs(Angle) - 15)/60)  # Total range is (75-15)=60
            # Graph Colors (complex shade gradient - this math leads to
            # appropriate boundary transitions by visual appearance)
            if(Score > 0.33):
                s = (Score-0.33)
                plotcols.append((1-s,0.84-(0.84*s),s))
            elif(Score < -0.33):
                s = (abs(Score)-0.33)
                plotcols.append((1, 0.84-(0.84*s),0))
                #print (plotcols[-1])
            else:
                #yellow
                plotcols.append((1.0, 0.84, 0))

        # now do the tally
        TotalWeight += Hypot
        TotalScore += Hypot * Score

    conc = np.round(100*TotalScore/TotalWeight,1)

    #  plot
    if (plot_TF):
        plt.rcParams.update({'font.size': 14})

        mX = max([abs(ele) for ele in DX])
        mY = max([abs(ele) for ele in DY])
        LIM = max(mX,mY) * 1.05

        plt.figure(figsize=(6,6))
        #circ = plt.Circle((0,0),ExlcusionLimit,color="lightgray",fill=False)
        #fig = plt.gcf()
        #ax = fig.gca()
        #ax.add_patch(circ)

        plt.ylim(-LIM,LIM)
        plt.xlim(-LIM,LIM)

        gtitle = "Error Field Trending = "+str(conc)
        if (graph_label != ""):
            gtitle = graph_label+"\n"+gtitle;

        plt.plot([-LIM,LIM],[-LIM,LIM],color="lightgray")
        plt.title(gtitle)
        if (XMeasName != ""):
            plt.xlabel(str(XMeasName))
        if (YMeasName != ""):
            plt.ylabel(str(YMeasName))

        for k in range(len(DX)):
            plt.scatter(DX[k],DY[k],alpha=min(1,200/len(DX)),
                        color=plotcols[k])

        #plt.text(-4,4,"Conc: "+str(conc))
        #plt.text(-4,3.5,"B/Y/R: ["+str(_b)+","+str(_y)+","+str(_r)+"]")
        #plt.text(-4,3,"Tot : "+str(len(DX)))

        plt.show()
    return conc


if __name__ == "__main__":

    print ("Creating Random Data Sample Plot")

    X = np.random.random_sample(1000)*5+2
    #Y= X + np.random.random_sample(100)*(X*0.35) - (X*0.175)
    Y = np.random.random_sample(1000)*5+2

    C = ErrorFieldConcordance(X,Y,True,"Random Noise Example")
    print ("--------------------------- Trends Exp")
    print ("ExB Conc:\t"+str(C)+"%")
