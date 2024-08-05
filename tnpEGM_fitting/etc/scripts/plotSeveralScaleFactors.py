#!/usr/bin/env python

import sys,os
from math import sqrt
import ROOT as rt
import libPython.CMS_lumi, libPython.tdrstyle


libPython.tdrstyle.setTDRStyle()


listOfFile = [
    { 'path' : 'results/eleID/ForJuan/Run2016BCD/passingMedium/egammaEffi.txt_EGM2D.root', 'legend' : 'runBCD 12.9/fb' , 'color' : rt.kAzure},
    { 'path' : 'results/eleID/ForJuan/Run2016EF/passingMedium/egammaEffi.txt_EGM2D.root' , 'legend' : 'runEF   7.2/fb' , 'color' : rt.kRed-2},
    { 'path' : 'results/eleID/ForJuan/Run2016GH/passingMedium/egammaEffi.txt_EGM2D.root' , 'legend' : 'runGH  13.6/fb' , 'color' : rt.kGreen+3},
]


grNames = [ 'grSF1D_0' ]


c = rt.TCanvas( 'SFs', 'SFs', 800, 500 )
c.SetTopMargin(0.10)
c.SetBottomMargin(0.15)
c.SetLeftMargin(0.12)

sfMin = 0.68
sfMax = 1.32


for igr in range(len(grNames)):
    legend = rt.TLegend(0.6,0.62,0.95,0.86)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)

    for ifile in range(len(listOfFile)):
        print 'Opening TFile: ', listOfFile[ifile]['path']
        rfile = rt.TFile.Open(listOfFile[ifile]['path'],'read')    
        rfile.Print()
        rgr   = rfile.Get(grNames[igr])

        drawOption = "P"
        if igr == 0 and ifile == 0 :
            drawOption = "AP"
            rgr.GetHistogram().SetMinimum(sfMin)
            rgr.GetHistogram().SetMaximum(sfMax)

        rgr.SetLineColor(   listOfFile[ifile]['color'] )
        rgr.SetMarkerColor( listOfFile[ifile]['color'] )
        c.cd()
        legend.AddEntry( rgr, listOfFile[ifile]['legend'],'PL' )
        rgr.Draw( drawOption )
    
    xMin = 0
    xMax = 2.6
    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    lineAtOne.Draw()
    legend.Draw()

libPython.CMS_lumi.lumi_13TeV = "33.7 fb^{-1}"
libPython.CMS_lumi.CMS_lumi(c, 4, 10)

c.Print('outEleID_SFs.pdf')
