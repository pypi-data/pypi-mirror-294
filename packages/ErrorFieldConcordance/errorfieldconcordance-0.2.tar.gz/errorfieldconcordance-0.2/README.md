# ErrorFieldConcordance

Thie package provides calculation (and optionally graphing) of trending concordance between two measures using the Error Field method.

This package requires numpy and matplotlib.

## Function Call
After importing the package, the method can be called as follows:

```
Concordance = ErrorFieldConcordance(X,Y,plot_TF=False,graph_label='',XMeasName='ΔX (LPM)',YMeasName='ΔY (LPM)')
```

The concordance value is a number in the range of \[-1,1\].  Values close to 1 indicate strong concordance.  Values close to -1 indicate strong negative concordance (i.e. the measures tend to move in the opposite direction of one another). Values near 0 suggest independence of the two measures. 

Function Parameters:
+ The X and Y parameters are lists or arrays of equal size corresponding to paired measures to be compared.
+ plot_TF is a boolean that controls whether or not a figure is created
+ graph_label is an optional parameter to be prefixed to the graph title
+ XMeasName and YMeasName are used to customize the X and Y graph labels


## Citing
Please cite this package using the following:  *PubMed Reference & Citation TBD*