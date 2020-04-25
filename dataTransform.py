# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:32:05 2020

@author: Borges
"""
import pylab
import csv
import itertools
import datetime
import calendar
#import matplotlib.dates as mdates

def load(file):
    date=[]
    cpi=[]
    inFile=open(file,'r',encoding="utf8")
    print("Loading...")
    
    for line in itertools.islice(csv.reader(inFile),26,329):
        dates=line[0].strip().split('-')
        date.append(datetime.datetime(int(dates[0]),int(dates[1]),int(dates[2])))
        cpi.append(float(line[1]))
        #date.append(line)  
        
    print("Data loaded")
    return date,cpi

def generate_models(x, y, degs):
    arrays=[]
    for d in degs:
        arrays.append(pylab.polyfit(x,y,d))
    return arrays

def se_over_slope(x,y,estimated,model):
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

def r_squared(y, estimated):
    mu = pylab.mean(y)
    SSE = pylab.sum((y-estimated)**2)
    SSW = pylab.sum((y-mu)**2)
    return 1-(SSE/SSW)

def evaluate_models_on_training(realDates,x, y, models):
    fig, ax = pylab.subplots()
    pylab.rcParams['lines.linewidth'] = 1
    pylab.rcParams['axes.titlesize'] = 10
    pylab.rcParams['axes.labelsize'] = 10
    pylab.rcParams['xtick.labelsize'] = 8
    pylab.rcParams['ytick.labelsize'] = 8
    pylab.rcParams['xtick.major.size'] = 8
    pylab.rcParams['ytick.major.size'] = 8
    pylab.rcParams['lines.markersize'] = 5
    pylab.rcParams['legend.numpoints'] = 1
    pylab.yticks(pylab.arange(min(cpi), max(cpi)+1, 3.0))
    ax.fmt_xdata = pylab.DateFormatter('%Y-%m-%d')
    ax.set_title('Canada CPI Inflation')
    pylab.xlabel('Date')
    fig.autofmt_xdate()
    pylab.ylabel('CPI')
    pylab.plot(date,cpi)
    for m in models:
        estYVals = pylab.polyval(m,x)
        r2 = r_squared(y,estYVals)
        std_error = se_over_slope(x,y,estYVals,m)
        pylab.plot(realDates,estYVals,label = 'Fit of degree '\
                   + str(len(m)-1)\
                       + ', R2 = '+str(round(r2,3)) + ', SE/S = '+str(round(std_error,3)))
    pylab.legend(loc = 'best')
    pylab.show()


def add_months(sourcedate, months): #courtesy of StackOverflow
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def predict(recentDate,models):
    newDates=[]
    estCPI=[]
    for i in range (24):
        newDates.append(add_months(recentDate,1))
        recentDate=newDates[-1]
    mplDates=pylab.date2num(newDates)
    for m in models:
        for x in mplDates:     
            estCPI.append(pylab.polyval(m,x))
    fig, ax = pylab.subplots()
    pylab.rcParams['lines.linewidth'] = 1
    pylab.rcParams['axes.titlesize'] = 10
    pylab.rcParams['axes.labelsize'] = 10
    pylab.rcParams['xtick.labelsize'] = 8
    pylab.rcParams['ytick.labelsize'] = 8
    pylab.rcParams['xtick.major.size'] = 8
    pylab.rcParams['ytick.major.size'] = 8
    pylab.rcParams['lines.markersize'] = 5
    pylab.rcParams['legend.numpoints'] = 1
    pylab.yticks(pylab.arange(min(estCPI), max(estCPI)+1, 0.5))
    ax.fmt_xdata = pylab.DateFormatter('%Y-%m-%d')
    ax.set_title('Projected Canada CPI Inflation')
    pylab.xlabel('Date')
    fig.autofmt_xdate()
    pylab.ylabel('Est. CPI')
    pylab.plot(newDates,estCPI)

date,cpi=load('CPI_MONTHLY.csv')
mplDates=pylab.date2num(date)
models=generate_models(mplDates, cpi, [1])
predict(date[-1],models)
#evaluate_models_on_training(date,mplDates, cpi, models)

