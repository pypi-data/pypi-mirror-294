from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import itertools as it
import math as m
import numpy as np
import sympy as sp
import os 

def color(txt,rgb):
    color_id = 16 + (36 * (rgb[0] // 51)) + (6 * (rgb[1] // 51)) + (rgb[2] // 51) 
    return "\033[38;5;"+str(color_id)+"m"+str(txt)+"\033[0m"

def digits(n):
    return [int(digit) for digit in list(str(n))]

def linear_regression(x_array,y_array):
    x_array = np.array(x_array).reshape(-1,1)
    y_array = np.array(y_array).reshape(-1,1)

    model = LinearRegression()
    model.fit(x_array,y_array)

    y0 = model.predict(np.array([1]).reshape(-1,1))[0][0]
    y1 = model.predict(np.array([2]).reshape(-1,1))[0][0]
    
    m=round(y1-y0,3)
    p=round(y0-m,3)

    return m,p

def derive(func):
    x = sp.symbols('x')
    f = func(x)
    f_prime = sp.diff(f, x)
    derivative_func = sp.lambdify(x, f_prime)
    return derivative_func

def primitive(func):
    x = sp.symbols('x')
    f = func(x)
    integral = sp.integrate(f, x)
    integral_func = sp.lambdify(x, integral)
    return integral_func

def integral(func,min,max):
    return primitive(func)(max) - primitive(func)(min)

def is_consecutive(array):
    if len(array) < 2:
        if len(array) == 1:
            return -1
        else:
            return 1
    
    for i in range(len(array) - 1):
        if abs(array[i] - array[i + 1]) != 1:
            return 0
    
    return 1

def bezout_coeff(a, b):
    def extended_gcd(a, b):
        s0, s1 = 1, 0
        t0, t1 = 0, 1
        r0, r1 = a, b
        while r1 != 0:
            q = r0 // r1
            r0, r1 = r1, r0 - q * r1
            s0, s1 = s1, s0 - q * s1
            t0, t1 = t1, t0 - q * t1
        return r0, s0, t0
    gcd_ab, x, y = extended_gcd(a, b)
    factor = m.gcd(a,b) // gcd_ab
    return x * factor, y * factor

def pq_maj(p, q):
    if len(p) != len(q) or sum(p) != sum(q):
        return -1
    
    for i in range(1, len(p)):
        if sum(p[:i]) < sum(q[:i]):
            return q
        if sum(p[:i]) > sum(q[:i]):
            return p

def p_avr(p,xi_array):
    n = len(xi_array)
    perm_ = list(it.permutations(range(n)))
    
    product_ = []
    for perm in perm_:
        product = 1
        for i in range(n):
            product *= xi_array[perm[i]] ** p[i]
        product_.append(product)
    
    avr = sum(product_) / m.factorial(n)
    return avr

def muirhead(p,q):
    min= q if pq_maj(p,q) == p else p
    print(str(min) + " ≺ " + str(pq_maj(p,q))) 
    print("=> "+str(p_avr(min,[10,50,8])) + " ≺ " + str(p_avr(pq_maj(p,q),[10,50,8])))

def size(file_name,system='decimal'):
    if system == 'decimal':
        d=1000
    if system == 'binary':
        d=1024
    s=os.path.getsize(file_name)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB' , 'EB', 'ZB', 'YB']:
        if s < d:
            return str(round(s,3)) + " " + x
        s /= d

def str_bin(string,space=True):
    if not space:
        binary_string = ''.join(format(ord(char), '08b') for char in string)
        return binary_string
    else:
        binary_string = ' '.join(format(ord(char), '08b') for char in string)
        return binary_string  

def map(value,fromLow,fromHigh,toLow,toHigh):
    x = (toHigh - toLow) / (fromHigh - fromLow)
    y = (toLow * fromHigh - fromLow * toHigh) / (fromHigh - fromLow)
    return x * value + y

def convert_base(number,base_from, base_to):
    r=[]
    hex_dict={10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
    try:
        b10 = int(str(number),base_from)
    except ValueError:
        result, temp, inside = [], '', False
        for char in str(number):
            if char == '(':
                if temp:
                    result.append(temp)
                temp, inside = '', True
            elif char == ')':
                result.append(temp)
                temp, inside = '', False
            else:
                temp += char
                if not inside:
                    result.append(temp)
                    temp = ''
        if temp:
            result.append(temp)
        b10=int(sum(base_from ** i * int(x) for i, x in enumerate(result[::-1])))
    if b10 == 0:
        return "0"
    while b10 > 0:
        if b10 % base_to <= 9:
            r.append(str(b10 % base_to))
        else:
                if base_to != 16:
                    r.append("("+str(b10 % base_to)+")")
                else:
                    r.append(hex_dict[b10 % base_to])
        b10 //= base_to
    r.reverse()
    return "".join(r)

def inv_dict(dict):
    return {v: k for k, v in dict.items()}

def plot(function,min,max,speed=0,verbose=False,error_verbose=False,color="blue",linestyle="solid",linewidth=1.5,scatter=False,scatter_color="red",scatter_size=20,step=0.01,show=True,fig=0):
    x_values=[]
    y_values=[]
    i = min

    if fig != 0:
        plt.figure(fig)

    while i<max:
        E=False
        error=""
        i=round(i,3)
        if is_int(i) == 1 :
            i=int(i)

        try:
            v=function(i)
            if v == None:
                E=True
        except Exception as e:
            E=True
            error=str(e)

        if E == False:
            x_values.append(i)
            y_values.append(function(i))

            if scatter:
                plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth)
                plt.scatter(x_values,y_values,c=scatter_color,s=scatter_size)
            else:
                plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth)

            if verbose:
                print(i,function(i))
            if speed != 0:
                plt.pause(speed)

        else:
            if error_verbose:
                print("Error at " + str(i),error)

        i+= step

    plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth,label=function.__name__)
    
    if show:
        plt.legend()
        plt.show()

def poly_plot(functions,colors,min,max,lines_style=[],lines_width=[],scatters=[],scatters_colors=[],scatters_size=[],steps=[],distinct=False):
    if not lines_style:
        lines_style = np.full((1,len(functions)),"solid")
        lines_style = lines_style[0]
    else:
        c=0
        for i in lines_style:
            if i == "":
                lines_style[c] = "solid"
            else:
                c+=1
    if not lines_width:
        lines_width = np.full((1,len(functions)),1.5)
        lines_width = lines_width[0]
    else:
        c=0
        for i in lines_width:
            if i == "":
                lines_width[c] = 1.5
            else:
                c+=1
    if not scatters:
        scatters = np.full((1,len(functions)),0)
        scatters = scatters[0]

    if not scatters_colors:
        scatters_colors = np.full((1,len(functions)),"red")
        scatters_colors = scatters_colors[0]
    else:
        c=0
        for i in scatters_colors:
            if i == "":
                scatters_colors[c] = "red"
            else:
                c += 1     
    if not scatters_size:
        scatters_size = np.full((1,len(functions)),20)
        scatters_size = scatters_size[0]
    else:
        c = 0
        for i in scatters_size:
            if i == "":
                scatters_size[c] = 20
            else:
                c+=1

    if distinct:
        for i in range(len(functions)):
            if scatters[i] == 1:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],scatter=True,scatter_color=scatters_colors[i],scatter_size=scatters_size[i],step=steps[i],show=False,fig=i+1)
                plt.legend()
            else:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],step=steps[i],show=False,fig=i+1)
                plt.legend()                
        plt.show()
    else:
        for i in range(len(functions)):
            if scatters[i] == 1:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],scatter=True,scatter_color=scatters_colors[i],scatter_size=scatters_size[i],step=steps[i],show=False)
                plt.legend()                 
            else:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],step=steps[i],show=False)
                plt.legend() 
        plt.show()

def ord(x, n):
    if m.gcd(x, n) != 1:
        return -1
    k = 1
    current = x % n
    while current != 1:
        current = (current * x) % n
        k += 1
        
    return k

def val(n,p):
    if is_int(n) == 1 and is_int(p) == 1:
        i=1
        while True:
            if n%(p**i) != 0:
                return i-1
                break
            elif n==0:
                return -1
            i+=1
    else:
        raise ValueError("Working for integers !")

def is_int(n):
    if int(n) == n:
        return 1
    else:
        return 0

def is_prime(n):   
    if n>=3:
        r=1
        for i in range(2,n):
            if n%i == 0:
                r = 0
                break
        return r
    elif n == 2:
        return 1
    elif n == 1 or n==0:
        return 0

def is_power(n,p):
    if is_int(n) == 1 and is_int(p) == 1:
        if int(n**(1/p)) == n**(1/p):
            return 1
        else:
            return 0
    else:
        raise ValueError("Input must be a positive integer.")
    
def is_sqrt(n):
    if is_int(n) == 1 and n >= 0:
        if int(m.sqrt(n)) == m.sqrt(n):
            return 1
        else:
            return 0
    else:
        raise ValueError("Input must be a positive integer.")

def phi(n):
    if is_int(n) == 0 or n <= 0:
        raise ValueError("Input must be a positive integer.")
    else:    
        result = n 
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result

def mobius(n):
    if n == 1:
        return 1
    for k in range(2, int(n**0.5) + 1):
        if n % (k * k) == 0:
            return 0
    prime_count = 0
    num = n
    for i in range(2, n + 1):
        if num % i == 0:
            prime_count += 1
            while num % i == 0:
                num //= i
        if num == 1:
            break
    if prime_count % 2 == 0:
        return 1
    else:
        return -1

def prime_counting(n):
    prime = [True] * (n+1)
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
    count = 0
    for p in range(2, n+1):
        if prime[p]:
            count += 1
    return count

def omega(n):
    if is_int(n) == 1:
        distinct_prime_factors = set()
        while n % 2 == 0:
            distinct_prime_factors.add(2)
            n = n // 2  
        for i in range(3, int(m.sqrt(n)) + 1, 2):
            while n % i == 0:
                distinct_prime_factors.add(i)
                n = n // i
        if n > 2:
            distinct_prime_factors.add(n)
        
        return len(distinct_prime_factors)
    else:
        raise ValueError("Working for integers")

def tau(n):
    if is_int(n) == 1:
        count = 0
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                if i == n // i:
                    count += 1
                else:
                    count += 2
        return count
    else:
        raise ValueError("Working for integers")
    
def sigma(n):
    if is_int(n) == 1:
        sum_divisors = 0
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                sum_divisors += i
                if i != n // i:
                    sum_divisors += n // i
        return sum_divisors
    else:
        raise ValueError("Working for integers")
    
def is_primitive_root(x, n):
    if m.gcd(x, n) != 1:
        return -1
    
    phi_n = phi(n)
    prime_factors = set()
    p = 2
    M = phi_n
    while p * p <= M:
        if M % p == 0:
            prime_factors.add(p)
            while M % p == 0:
                M //= p
        p += 1
    if M > 1:
        prime_factors.add(M)

    for factor in prime_factors:
        if pow(x, phi_n // factor, n) == 1:
            return 0
    
    if pow(x, phi_n, n) == 1:
        return 1

def mod_period(mod_n, func):
    i = 0
    r = []
    while True:
        r.append(func(i) % mod_n)
        i += 1
        if func(i) % mod_n in r:
            break
    return sorted(r)

def sym_mod(mod_n, func):
    half_mod = mod_n / 2
    symmetric_values = [v if v <= half_mod else v - mod_n for v in mod_period(mod_n,func)]
    principal_values = [v for v in symmetric_values if v >= 0]
    return sorted(principal_values)

def divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

def decompose(n):
    def get_prime_factors(n):
        factors = {}
        while n % 2 == 0:
            if 2 in factors:
                factors[2] += 1
            else:
                factors[2] = 1
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                if i in factors:
                    factors[i] += 1
                else:
                    factors[i] = 1
                n //= i
        if n > 2:
            factors[n] = 1
        return factors
    def format_decomposition(factors):
        terms = []
        for prime, exponent in sorted(factors.items()):
            if exponent > 1:
                terms.append(f"{prime}^{exponent}")
            else:
                terms.append(f"{prime}")
        return " * ".join(terms)
    
    factors = get_prime_factors(n)
    return format_decomposition(factors)

def legendre(a, p):
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

def tonelli_shanks(n, p):
    """ Find a square root of n modulo p using the Tonelli-Shanks algorithm. """
    assert legendre(n, p) == 1, "n is not a quadratic residue modulo p"
    if n == 0:
        return 0
    if p == 2:
        return n
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    while t != 0 and t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    
    return r

def smallest_qr(a, p):
    if p <= 2 or p % 2 == 0:
        raise ValueError("p must be an odd prime.")
    a = a % p
    if a == 0:
        return 0
    if a == 1:
        return 1
    if legendre(a, p) == 1:
        x = tonelli_shanks(a, p)
        smallest_x = min(x, p - x)
        return smallest_x
    else:
        raise ValueError(f"No quadratic residue congruent to {a} modulo {p} found.")

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_(x,min,max):
    return (max + min*np.exp(-x))/(1+np.exp(-x))

def logit(x):
    return np.log(x/(1-x))

def logit_(x,min,max):
    return np.log((x-min)/(max-x))

