## Toom-Cook 3-way algorithm realisation

Toom cook algorithm is the advanced approach for splitting the numbers into parts. It is based on the Karatsuba method by splitting each number to be multiplied
into multiple parts.

Algorithm improves the bit complexity of mutiplication of two large positive integers. 

### Details
Assume that we have two integers written in terms of polynomials: 

![equation](assets/1.svg) \
![equation](assets/2.svg) 

![equation](assets/3.svg)

As we are doing Toom-3, we choose k = 3. 
Let the operands considered are split into 3 pieces of equal length: 

![equation](assets/4.svg) \
![equation](assets/5.svg)

```python
# P(x) = a2 * x^2 + a1 * x + a0
a2 = a[(length * 2 // 3):                 ]
a1 = a[  (length // 3)  :(length * 2 // 3)]
a0 = a[                 :  (length // 3)  ]

# Q(x) = b2 * x^2 + b1 * x + b0
b2 = b[(length * 2 // 3):                 ]
b1 = b[  (length // 3)  :(length * 2 // 3)]
b0 = b[                 :  (length // 3)  ]
```

The purpose of defining these polynomials is that if we can compute their product: 

![equation](assets/6.svg) \
![equation](assets/7.svg)

The final r(x) is calculated through the value of x, although the final step is going to be the addition.
p(x) and q(x) are calculated and multiplied by choosing some set of points, forming r(x).

In Toom-3 example, we will use the points (0, 1, −1, −2, and ∞). These choices simplify evaluation, producing the formulas: 

![equation](assets/8.svg) \
![equation](assets/9.svg) \
![equation](assets/10.svg) \
![equation](assets/11.svg) \
![equation](assets/12.svg) 

![equation](assets/13.svg) \
![equation](assets/14.svg) \
![equation](assets/15.svg) \
![equation](assets/16.svg) \
![equation](assets/17.svg) 

```python
# p(0) = a0, q(0) = b0
a_0, b_0 = a0, b0

# p(1) = a0 + a1 + a2, q(1) = b0 + b1 + b2
for i in range(length // 3):
    a_1.append(a0[i] + a1[i] + a2[i])
    b_1.append(b0[i] + b1[i] + b2[i])

# p(-1) = a0 - a1 + a1, q(1) = b0 - b1 + b2
for i in range(length // 3):
    a_m1.append(a0[i] - a1[i] + a2[i])
    b_m1.append(b0[i] - b1[i] + b2[i])

# p(-2) = a0 - 2 * a1 + 4 * a2, q(1) = b0 - 2 * b1 + 4 * b2
for i in range(length // 3):
    a_m2.append(a0[i] - (a1[i] << 1) + (a2[i] << 2))
    b_m2.append(b0[i] - (b1[i] << 1) + (b2[i] << 2))

# p(inf) = a2, q(inf) = b2
a_inf, b_inf = a2, b2
```
Then: 

![equation](assets/18.svg) \
![equation](assets/19.svg) \
![equation](assets/20.svg) \
![equation](assets/21.svg) \
![equation](assets/22.svg) 
```python
# c(0) = a(0) * b(0)
c_0   = self.multiply(a_0, b_0)
# c(1) = a(1) * b(1)
c_1   = self.multiply(a_1, b_1)
# c(-1) = a(-1) * b(-1)
c_m1  = self.multiply(a_m1, b_m1)
# c(-2) = a(-2) * b(-2)
c_m2  = self.multiply(a_m2, b_m2)
# c(inf) = a(inf) * b(inf)
c_inf = self.multiply(a_inf, b_inf)
```

Furthermore, we need to determine coefficients of R(X).  
A difficult design challenge in Toom–Cook is to find an efficient sequence of operations to compute this product; one sequence given by [Bodrato](http://www.bodrato.it/toom-cook/) for Toom-3 is the following:

```python
'''
r0 = c(0)
r4 = c(inf)
r3 = (c(-2) - c(1)) // 3
r1 = (c(1) - c(-1)) // 2
r2 = c(-1) - c(0)
r3 = (r2 - r3) // 2 + 2 * r4 = (-c(-2) + 3 * c(-1) - 3 * c(0)  + c(1) + 12 * c(inf)) / 6
r2 = r2 + r1 - r4            = (3 * c(-1)) - 6 * c(0) + 3 * c(1) - 12 * c(inf)) / 6
r1 = r1 - r3 = r1 - r3       =  (c(-2) - 6 * c(-1) + 3 * c(0) + 2 * c(1) - 12 * c(inf)) / 6
'''

# r3 = (-c(-2) + 3 * c(-1) - 3 * c(0)  + c(1) + 12 * c(inf)) / 6
for i in range((length // 3) * 2):
    c  = -c_m2[i]                               # - c(-2)
    c += (c_m1[i] << 1) + c_m1[i]               # + c(-1)  * 3
    c -= (c_0[i] << 1) + c_0[i]                 # - c(0)   * 3
    c += c_1[i]                                 # + c(1)
    c += (c_inf[i] << 3) + (c_inf[i] << 2)      # + c(inf) * 12 
    c  = c // 6                                 # / 6
    r3.append(c)    
    
# r2 = (3 * c(-1) - 6 * c(0) + 3 * c(1) - 6 * c(inf)) / 6
for i in range((length // 3) * 2):              
    c  = (c_m1[i] << 1) + c_m1[i]               # + c(-1)  * 3
    c -= (c_0[i] << 2) + (c_0[i] << 1)          # - c(0)   * 6
    c += (c_1[i] << 1) + c_1[i]                 # + c(1)   * 3
    c -= (c_inf[i] << 2) + (c_inf[i] << 1)      # - c(inf) * 6
    c  = c // 6                                 # / 6
    r2.append(c)
    
# r1 = (c(-2) - 6 * c(-1) + 3 * c(0) + 2 * c(1) - 12 * c(inf)) / 6
for i in range((length // 3) * 2):
    c  = c_m2[i]                                # + c(-2)
    c -= (c_m1[i] << 2) + (c_m1[i] << 1)        # - c(-1)  * 6
    c += (c_0[i] << 1) + c_0[i]                 # + c(0)   * 3
    c += (c_1[i] << 1)                          # + c(1)   * 2
    c -= (c_inf[i] << 3) + (c_inf[i] << 2)      # - c(inf) * 12
    c  = c // 6                                 # / 6
    r1.append(c)

# r0 = c(0)
r0 = c_0

# r4 = c(inf)
r4 = c_inf 
```

### Complexity

Toom-3 running time is significally
![equation](assets/23.svg), resembles 5 multiplies for 3 splits of each size.

This is an advance over Karatsuba algorithm which runs at ![equation](assets/23.svg)
