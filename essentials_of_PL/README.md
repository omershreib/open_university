# How to Run Scheme With *EOPL*

### Step #1:

install Jupyter Notebook and Calysto Scheme 

```commandline
pip install jupyter
pip install calysto-scheme
python -m calysto_scheme install
```

Then in Jupyter Notebook:

Select Kernel → Change Kernel → Calysto Scheme

### Step #2:

install **Racket** with the *iracket* kernel

```commandline
raco pkg install iracket
iracket install --user
```

### Step #3

install `racket-jupyter` kernel

```commandline
raco pkg install racket-jupyter
racket -l racket-jupyter install
```


### Step #4:

install EOPL:

```commandline
raco pkg install eopl
```

finally, run jupyter:

```commandline
jupyter notebook
```
