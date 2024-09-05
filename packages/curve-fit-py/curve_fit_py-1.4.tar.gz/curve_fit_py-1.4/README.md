# curve_fit_py
A package designed to Find the coefficients of a function $f(x)$ that best fits an array of data points.

## Table of contents
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
- [License](#license)

## Installation
1. Open terminal in vs code

2. Input ``pip install curve_fit_py`` and press enter

## Usage
The package can be used in a couple of ways depending on what you want to do.
The function for curve fitting is ``curve_fit_py.curve_fit(data,x,type,degree,model,p0)``. Not all parameters need to be used, it depends. 
The package provides 3 built-in function types:
1. **Polynomial**
2. **Exponential**
3. **Natural logarithmic**

which can be used with

 ``'polynomial'``, ``'exp'``  and ``'ln'``. If provided ``type = 'polynomial'``, setting a degree to some value is required. Otherwise, not. If one of these types is used, the parameters ``model`` and ``p0`` are not to be used. After applying the function, you can equate it to your coefficients, for example $a,b$ and graph it.

 Here's a simple example on how to use it:

 ```
 import numpy as np
 import matplotlib as plt
 from curve_fit_py import curve_fit

 sample = np.array([1,2,3,4,5,6,7,8,9,10]) 
 x = np.arange(1,11) # Obviously a 1 degree polynomial, i.e a line.
 a,b = cfp(data=sample,x=x, type='polynomial',degree=1)

 t = np.linspace(1,10,50)
 fig, ax = plt.subplots()
 plt.grid()
 plt.scatter(x,sample,color='red')
 plt.plot(t,a*t + b, color='black')
 plt.show()
```

However, not everybody needs one of these types of functions. Maybe somebody requires a sin function of the type $A\sin(bx)$. In that case, we will not be using ``type`` or ``degree``, no. We will be using a model function, in our case $A\sin(bx)$, and an initial guess for the coefficients $A$ and $b$ stored in the array $p_0$. Here's a simple example:"

```
 import numpy as np
 import matplotlib as plt
 from curve_fit_py import curve_fit

def sin_model(x,a,b):
    return a*np.sin(b*x)

 sample = np.array([0,5,10,5,0,-5,-10,-5,0]) 
 x = np.arange(0,10) # Obviously a sin function.
 a,b = cfp(data=sample,x=x,model = sin_model, p0 =[10,0.69])

 t = np.linspace(0,10,50)
 fig, ax = plt.subplots()
 plt.grid()
 plt.scatter(x,sample,color='red')
 plt.plot(t,sin_model(t,a,b), color='black')
 plt.show()
```

## How it works

The package uses multiple techniques for approximating a curve given a data set.

If the user has provided a type of function in the parameters, the initial guess for the coefficients will be done through least squares, i.e won't be really a guess but a first approximation. It works the following way for a 1 degree polynomial:

$$Ax = b$$

$$\begin{bmatrix}x_1 & 1 \\\ x_2 & 1 \\\ \vdots & \vdots \\\ x_i & 1 \end{bmatrix} \begin{bmatrix} a \\\ b \end{bmatrix} = \begin{bmatrix} y_1 \\\ y_2 \\\ \vdots \\\ y_i \end{bmatrix}$$

In which $x_i$ and $y_i$ are entries from the arrays ``data`` and ``x`` provided. Given that we can't possibly find the inverse of $A$ and solve the equation, we must apply the least square method to give us an approximate answer. That would be:

$$x = (A^TA)^{-1}A^Tb$$

However this doesn't always give a good approximation. In cases with an exponential or log function, we have to apply a second technique in order to get a better estimate after we've applied least squares. That technique is called Gauss-Newton's method. It works the following way:

Imagine we have a matrix with already existing initial approximations/guesses called $p_0$. Say we only have one component or a bunch of them under one name - $\theta$. We now define a new variable, called a residual: $r_i = y_i - f(x_i,\theta)$ in which $f$ is the function that is attempting to approximate the data set. After that we define a matrix $J$ in which we have entries:

$$J = \begin{bmatrix} \frac{\partial r_i}{\partial \theta} \\\ \vdots \end{bmatrix}$$

We multiply $J$ by a matrix called $\Delta \theta$ and we equate to the matrix of residuals $r$.

$$ \begin{bmatrix} \frac{\partial r_i}{\partial \theta} \\\ \vdots \end{bmatrix} \begin{bmatrix} \Delta \theta \end{bmatrix} = \begin{bmatrix} r_i \\\ \vdots \end{bmatrix}$$

We solve for $\Delta \theta$ using the least square method and we get a solution which tells us by how much we should multiply the derivative of $r_i$ with respect to $\theta$ to get the currently existing residual or error of $r_i$. If we do that in the opposite direction, we should get 0 error

If we change the already existing parameters of $r_i$ with new ones $\theta_f = \theta_i - \Delta \theta$ However we can't do that change too drastically because its not always possible to have an error of 0. Instead we apply a learning rate $l_r$ such that:

$$\theta_f = \theta_i - l_r \Delta \theta$$

and we iterate it a couple of times until it converges to some final error which is the minimum.

## License

This package is licensed under the [MIT License](LICENSE.txt)