import pandas as pd
from verstack import LGBMTuner

df = pd.read_csv('/Users/danil/Documents/data/titanic/pp_titanic_train.csv')
X = df.drop('target', axis = 1)
y = df.target

model = LGBMTuner(
    metric = 'accuracy', 
    trials = 2, 
    verbosity = 0, 
    visualization = False
    )
model.fit(X, y)


from verstack.tools import timer

@timer
def do_stuff(verbose=False):
    for i in range(1000000):
        j = i**2

do_stuff(verbose=False)


class Dummy:

    def __init__(self, verbose):
        self.verbose = verbose
    @timer
    def do_stuff(self):
        for i in range(1000000):
            j = i**2
        print(j)

d = Dummy(True)

d.do_stuff()

fs = FeatureSelector(objective = 'classification', verbose=False)


_=fs.fit_transform(X,y)