import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

loansData = pd.read_csv('loansData.csv')

def dataProcessor(data):

    def strCleaner(data, remItem, objType):
        def remFunc(x):
            newStr = x.translate(None, remItem)

            if objType == "float":
                return round(float(newStr) / 100, 4)
            elif objType == "int":
                return int(newStr)
            else:
                return newStr

        newArr = map(remFunc,data)
        return newArr


    def ficoCleaner(data, delim):
        def strToArr(word):
            return word.split(delim)

        def outTupsFirst(tup):
            return int(tup[0])

        tupsArr = map(strToArr,data)

        newArr = map(outTupsFirst, tupsArr)

        # print tupsArr
        # print newArr
        return newArr


    data['Interest.Rate'] = strCleaner(data['Interest.Rate'], '%', 'float')
    data['Loan.Length'] = strCleaner(data['Loan.Length'], 'months', 'int')
    data['FICO.Score'] = ficoCleaner(data['FICO.Range'],'-')

    return data

loansData =  dataProcessor(loansData)

# plt.figure()

# p = loansData['FICO.Score'].hist()
# a = pd.scatter_matrix(loansData, alpha=0.5, figsize=(10,10), diagonal='hist')

# plt.show()

plt.figure()

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

x = np.column_stack([x1, x2])

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()

print f.summary()