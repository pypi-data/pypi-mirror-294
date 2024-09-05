import numpy as np

def exp_func(x,a,b):
    return a*np.exp(b*x)

def error_function_exp(x,y,a,b):
    approximation = exp_func(x,a,b)
    residual = y-approximation
    return np.sum(residual**2)

def Jacobian_exp(x,a,b):
    J_a = -np.exp(b*x)
    J_b = -a*x*np.exp(b*x)
    J = np.column_stack((J_a,J_b))
    return J

def Jacobian_ln(x,a,b):
    J_a = -np.log(b*x)
    t = np.ones(len(J_a))
    J_b = -(a/b)*t
    J = np.column_stack((J_a,J_b))
    return J

def ln_func(x,a,b):
    return a*np.log(b*x)

def error_function_ln(x,y,a,b):
    approximation = ln_func(x,a,b)
    residual = y - approximation
    return np.sum(residual**2) 

def curve_fit(data,x,type=None,degree=None,model=None,p0=None):   # curve fit function
    """
    Finds the coefficients of a function **f(x)** that best fits an array of data points.
    Parameters:
        data (array): Data points on the y-axis.
        x (array): Data points on the x-axis.
        type (str): Type of the function that will best fit the data points. Polynomial, exp(exponential) or ln(natural logarithmic).
        degree (int): Optional. Only required if function type is a polynomial.
        model (function): The type of function we want to fit on a given data set (Only if a type is not provided.)
        p0 (array): An initial guess for the coefficients of the curve. (Only if a model is provided)

    Returns:
        A row or column shaped array with entries being equal to each coefficient - **a**,**b**,**c**, etc.

    Example:
        >>> sample = np.array([1,2,3,4,5,6,7,8,9,10]) (This is obviously a 1 degree polynomial, i.e a line)
        >>> x = np.array([1,2,3,4,5,6,7,8,9,10])
        >>> a, b = curve_fit(sample,x,'polynomial', 1)
        >>> t = np.linspace(0,10,50)
        >>> y = a*t + b
        One can then plot it using matplotlib.pyplot

    """
    if type != 'polynomial':
        degree = None
    if type == None:
        model is not None
        p0 is not None
    if model is None and p0 is None:
        type is not None
    if type == 'polynomial':
        A = np.zeros((len(data),degree+1))
        for i in range(0,len(data)):
            for j in range(0,degree+1):
                A[i,j] = x[i]**(degree-j)
        np.transpose(data)
        y = np.linalg.inv(np.transpose(A)@A)@(np.transpose(A)@data)
        return y
    if type == 'exp':
        A = np.column_stack((np.ones(len(data)), x))
        data = np.log(data)
        data = np.transpose(data)
        y = np.linalg.inv(np.transpose(A)@A)@(np.transpose(A)@data)
        y[0] = np.exp(y[0])
        data = np.exp(data)
        data = np.transpose(data)
        learning_rate = 0.01
        tolerance = 0.01
        max_iterations = 1000
        previous_error = error_function_exp(x,data,y[0],y[1])
        for i in range(max_iterations):
            residuals = data - exp_func(x,y[0],y[1])
            J = Jacobian_exp(x,y[0],y[1])
            JTJ = np.transpose(J)@J
            JTr = np.transpose(J)@residuals
            if np.linalg.det(JTJ) == 0:
                return y
            delta_params = np.linalg.inv(JTJ)@JTr
            y = y - learning_rate*delta_params
            new_error = error_function_exp(x,data,y[0],y[1])
            if new_error == previous_error:
                return y
            previous_error = new_error
            if new_error <= tolerance:
                return y
        return y
    if type == 'ln':
        A = np.ones((len(data),2))
        for i in range(0,len(data)):
            A[i,1] = np.log(x[i])
        np.transpose(data)
        y = np.linalg.inv(np.transpose(A)@A)@(np.transpose(A)@data)
        y[0] = np.exp(y[0]/y[1])
        learning_rate = 0.01
        tolerance = 0.01
        max_iterations = 1000
        previous_error = error_function_ln(x,data,y[0],y[1])
        for i in range(max_iterations):
            residuals = data - ln_func(x,y[0],y[1])
            J = Jacobian_ln(x,y[0],y[1])
            JTJ = np.transpose(J)@J
            JTr = np.transpose(J)@residuals
            if np.linalg.det(JTJ) == 0:
                return y
            delta_params = np.linalg.inv(JTJ)@JTr
            y = y - learning_rate*delta_params
            new_error = error_function_ln(x,data,y[0],y[1])
            if new_error == previous_error:
                return y
            previous_error = new_error
            if new_error <= tolerance:
                return y
        return y
    if type == None:
        learning_rate = 0.01
        tolerance = 0.01
        max_iterations = 1000
        params = p0
        epsilon = 1e-7
        params_alt = np.ones(len(p0))
        J = np.zeros((len(data),len(p0)))
        for i in range(max_iterations):
            residuals = data - model(x,*params)
            for k in range(0,len(data)):
                for j in range(0,len(p0)):
                    params_alt[j] = params[j] + epsilon
                    J[k,j] = - ((model(x[k],*params_alt) - model(x[k],*params))/epsilon)
                    params_alt[j] = params[j]
            JTJ = np.transpose(J)@J
            JTr = np.transpose(J)@residuals
            if np.linalg.det(JTJ) == 0:
                return y
            delta_params = np.linalg.inv(JTJ)@JTr
            params = params - learning_rate*delta_params
        return params