#===============================================================================================
#Note for v1:
#The script is used to plot the Bz field distribution at R and Z coordinate for simulated field.
#
#By Aiqiang Guo -- 2016/05/25
#===============================================================================================
#Note for v2:
#The script is used to plot the gradient of B field distribution at R and Z coordinate for simulat
#-ed field.
#
#By Aiqiang Guo -- 2016/05/25
#===============================================================================================
#Note for v3:
#The script is used to plot the comparison of B field distribution in Calculation and Simulation
#
#By Aiqiang Guo -- 2016/06/08
#===============================================================================================

from ROOT import gStyle, gSystem, gROOT, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TH1, kRed, kBlue, kBlack, kGreen, kYellow, TLegend
import numpy as np
#import rootnotes
#import rootprint
#import utils

gROOT.Reset()
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
gStyle.SetTitleOffset(1.5,"xyz")
gSystem.Load("libMathMore")
#====================================================================
#Strategy: 1. build the list by selected data
#          2. transform the list to be array by array command
#	   3. loop the array to calculat the grediant of the B field.
#====================================================================

Bz2D = TH2F("Bz2D","Bz", 301,-2.0,1.0, 121,0,1.2)
Bz2D.GetXaxis().SetTitle("Z / m")
Bz2D.GetYaxis().SetTitle("R / m")
Bz2D.GetZaxis().SetTitle("Bz / T")
Bz2D.GetXaxis().CenterTitle()
Bz2D.GetYaxis().CenterTitle()
Bz2D.GetZaxis().CenterTitle()

dBzdz2D = TH2F("dBzdz2D","dBz/dz", 300,-2.0,1.0, 121,0,1.2)
dBzdz2D.GetXaxis().SetTitle("Z / m")
dBzdz2D.GetYaxis().SetTitle("R / m")
dBzdz2D.GetZaxis().SetTitle("dBz/dz / T")
dBzdz2D.GetXaxis().CenterTitle()
dBzdz2D.GetYaxis().CenterTitle()
dBzdz2D.GetZaxis().CenterTitle()


# This is what you would normally do in pyroot
c1 = TCanvas( 'c1', 'Example with Formula', 800, 600 )
# This is to draw the canvas embedded in the notebook
#c1 = rootnotes.canvas("Example with Formula", (800, 600))

Bz = []

import re
fname = "../Simulation/160128-10-2_cylindrical_inner.table"
f = open(fname,'r')
next(f)
for line in f:
    eline = line.split()
    noline = [float(x) for x in eline]
    #print eline
    if(noline[1] != 6.0): continue
    #print noline
    #print noline[6]+noline[7]
    #Bz.Fill(noline[0],noline[2],noline[3])
    #Bz1D.Fill(noline[2],noline[5])
    #binx = int(noline[0]/0.01) + 1
    #biny = int((noline[2]+2.0)/0.01) + 1
    binx = round(noline[0]/0.01 + 1)
    biny = round((noline[2]+2.0)/0.01 + 1)
    #print binx,biny, noline[5]
    #print noline[0], noline[2], noline[5], binx, biny, int(binx), int(biny)
    Bz2D.SetBinContent(int(binx), int(biny), noline[5])
    Bz.append(noline[5])

#Bz2D.Rebin2D(2,2)
#Bz2D.Scale(1./4)
#Bz2D.Draw("SURF1")
##Bz2D.Draw("CONT1Z")
#c1.Print("Bz2D.eps")
#c1.Print("Bz2D.pdf")
##c1

#================================================
# transform the list to array
#================================================

ABz = np.array(Bz)
ABz.shape = (301,121)
print ABz

#================================================
# loop the array to draw the Bz distribution
#================================================

for i in range(301):
    for j in range(121):
        print i, j
        Bz2D.SetBinContent(i, j, ABz[i,j])

Bz2D.Rebin2D(2,2)
Bz2D.Scale(1./4)
Bz2D.Draw("SURF1")

c1.Print("Bz2D_v2.pdf")

#================================================
# loop the array to draw the dBz/dz distribution
#================================================
step = 0.01
for i in range(300):
    for j in range(121):
        print i, j
        dBz = ABz[i+1,j] - ABz[i,j]
        dBzdz = dBz/step
        dBzdz2D.SetBinContent(i+1, j+1, dBzdz)

dBzdz2D.Rebin2D(2,2)
dBzdz2D.Scale(1./4)
dBzdz2D.Draw("SURF1")

c1.Print("dBzdz2D_v2.pdf")

bin10 = int(round(0.1/0.01))
bin20 = int(round(0.2/0.01))
bin30 = int(round(0.3/0.01))
bin40 = int(round(0.4/0.01))
bin50 = int(round(0.5/0.01))

print bin10, bin20, bin30, bin40, bin50

dBzdz_r_1 = dBzdz2D.ProjectionX("dBdz_r_1",bin10,bin10)
dBzdz_r_2 = dBzdz2D.ProjectionX("dBdz_r_2",bin20,bin20)
dBzdz_r_3 = dBzdz2D.ProjectionX("dBdz_r_3",bin30,bin30)
dBzdz_r_4 = dBzdz2D.ProjectionX("dBdz_r_4",bin40,bin40)
dBzdz_r_5 = dBzdz2D.ProjectionX("dBdz_r_5",bin50,bin50)


dBzdz_r_1.SetMinimum(-0.3)
dBzdz_r_1.SetMaximum(0.3)
dBzdz_r_1.GetYaxis().SetTitle("dBz/dz T")


dBzdz_r_1.SetLineColor(kYellow)
dBzdz_r_2.SetLineColor(kRed)
dBzdz_r_3.SetLineColor(kBlack)
dBzdz_r_4.SetLineColor(kBlue)
dBzdz_r_5.SetLineColor(kGreen)


dBzdz_r_1.Draw("C")
dBzdz_r_2.Draw("C,same")
dBzdz_r_3.Draw("C,same")
dBzdz_r_4.Draw("C,same")
dBzdz_r_5.Draw("C,same")

leg =TLegend(0.4,0.8,0.6,0.6);
leg.AddEntry(dBzdz_r_1,  "r = 10 cm",  "l");
leg.AddEntry(dBzdz_r_2,  "r = 20 cm",  "l");
leg.AddEntry(dBzdz_r_3,  "r = 30 cm",  "l");
leg.AddEntry(dBzdz_r_4,  "r = 40 cm",  "l");
leg.AddEntry(dBzdz_r_5,  "r = 50 cm",  "l");
leg.SetFillColor(0);
leg.Draw();


c1.Print("dBzdz_r_0_v2.pdf")




