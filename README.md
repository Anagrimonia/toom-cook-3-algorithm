## Toom-Cook 3-way algorithm realisation

Toom cook algorithm is the advanced approach for splitting the numbers into parts. The Actually based on the Karatsuba method by splitting each number to be multiplied
into multiple parts.

Algorithm improves the bit complexity of mutiplication of two large positive integers. 

### Details
Assume that we have two integers written in terms of polynomials: \
![equation](https://latex.codecogs.com/svg.latex?A%20%3D%20a_%7Bn-1%7D*x%5E%7Bn-1%7D&plus;%20...%20&plus;a_%7B1%7D%20*%20x%5E%7B%7D%20&plus;%20a_%7B0%7D) \
![equation](https://latex.codecogs.com/svg.latex?B%20%3D%20b_%7Bn-1%7D*x%5E%7Bn-1%7D&plus;%20...%20&plus;b_%7B1%7D%20*%20x%5E%7B%7D%20&plus;%20b_%7B0%7D) 

![equation](https://latex.codecogs.com/svg.latex?n%20%3D%20k%5Em%2C%20m%20%3E%200)

As we are doing Toom-3, we choose k = 3. 
Let the operands considered are split into 3 pieces of equal length: \
![equation](https://latex.codecogs.com/svg.latex?p%28x%29%20%3D%20a_%7B2%7D*x%5E%7B2%7D&plus;%20a_1*x%20&plus;%20a_%7B0%7D)
![equation](https://latex.codecogs.com/svg.latex?q%28x%29%20%3D%20b_%7B2%7D*x%5E%7B2%7D&plus;%20b_1*x%20&plus;%20b_%7B0%7D)

The purpose of defining these polynomials is that if we can compute their product: \
![equation](https://latex.codecogs.com/svg.latex?r%28x%29%20%3D%20p%28x%29*%20q%28x%29)
![equation](https://latex.codecogs.com/svg.latex?R%28x%29%20%3D%20r_4%20*%20x%5E4%20&plus;%20r_3%20*%20x%5E3%20&plus;%20r_2%20*%20x%5E2%20&plus;%20r_1%20*%20x%5E1%20&plus;%20r_0)

The final r(x) is calculated through the value of x, although the final step is going to be the addition.
p(x) and q(x) are calculated and multiplied by choosing some set of points, forming r(x).

In Toom-3 example, we will use the points (0, 1, −1, −2, and ∞). These choices simplify evaluation, producing the formulas: 

![equation](https://latex.codecogs.com/svg.latex?p%280%29%20%3D%20m_0%20&plus;%20m_1%280%29&plus;m_2%280%29%5E2%20%3D%20m_0) \
![equation](https://latex.codecogs.com/svg.latex?p%281%29%20%3D%20m_0%20&plus;%20m_1%281%29&plus;m_2%281%29%5E2%20%3D%20m_0%20&plus;%20m_1%20&plus;%20m_2) \
![equation](https://latex.codecogs.com/svg.latex?p%28-1%29%20%3D%20m_0%20&plus;%20m_1%28-1%29&plus;m_2%28-1%29%5E2%20%3D%20m_0%20-%20m_1%20&plus;%20m_2) \
![equation](https://latex.codecogs.com/svg.latex?p%28-2%29%20%3D%20m_0%20&plus;%20m_1%28-2%29&plus;m_2%28-2%29%5E2%20%3D%20m_0%20-%202m_1%20&plus;%204m_2) \
![equation](https://latex.codecogs.com/svg.latex?p%28%5Cinfty%29%20%3D%20m_2) 

![equation](https://latex.codecogs.com/svg.latex?q%280%29%20%3D%20n_0&plus;n_1%280%29&plus;n_2%280%29%5E2%20%3D%20n_0) \
![equation](https://latex.codecogs.com/svg.latex?q%281%29%20%3D%20n_0&plus;n_1%281%29&plus;n_2%281%29%5E2%20%3D%20n_0%20&plus;%20n_1%20&plus;%20n_2) \
![equation](https://latex.codecogs.com/svg.latex?q%28-1%29%20%3D%20n_0&plus;n_1%28-1%29&plus;n_2%28-1%29%5E2%20%3D%20n_0%20-%20n_1%20&plus;%20n_2) \
![equation](https://latex.codecogs.com/svg.latex?q%28-2%29%20%3D%20n_0&plus;n_1%28-2%29&plus;n_2%28-2%29%5E2%20%3D%20n_0%20-%202n_1%20&plus;%204n_2) \
![equation](https://latex.codecogs.com/svg.latex?q%28%5Cinfty%29%20%3D%20n_2) 

Then: 

![equation](https://latex.codecogs.com/svg.latex?r%280%29%20%3D%20m_0%20*%20n_0) \
![equation](https://latex.codecogs.com/svg.latex?r%281%29%20%3D%20%28m_0%20&plus;%20m_1%20&plus;%20m_2%29%20*%20%28n_0%20&plus;%20n_1%20&plus;%20n_2%29) \
![equation](https://latex.codecogs.com/svg.latex?r%28-1%29%20%3D%20%28m_0%20-%20m_1%20&plus;%20m_2%29%20*%20%28n_0%20-%20n_1%20&plus;%20n_2%29) \
![equation](https://latex.codecogs.com/svg.latex?r%28-2%29%20%3D%20%28m_0%20-%202m_1%20&plus;%204m_2%29%20*%20%28n_0%20-%202n_1%20&plus;%204n_2%29) \
![equation](https://latex.codecogs.com/svg.latex?r%28%5Cinfty%29%20%3D%20m_2%20*%20n_2) 



### Complexity

Toom-3 running time is significally
![equation](https://latex.codecogs.com/svg.latex?O%28n%5E%7B%5Cfrac%7Blog%285%29%7D%7Blog%283%29%7D%7D%29%20%3D%20O%28n%5E%7B1.465%7D%29), resembles 5 multiplies for 3 splits of each size.

This is an advance over Karatsuba algorithm which runs at ![equation](https://latex.codecogs.com/svg.latex?O%28n%5E%7B%5Cfrac%7Blog%283%29%7D%7Blog%282%29%7D%7D%29%20%3D%20O%28n%5E%7B1.585%7D%29)
