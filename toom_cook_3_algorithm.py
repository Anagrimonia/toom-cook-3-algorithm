import sys
import traceback

class ToomCook3:
    def __init__(self, limit = 729):
        self.limit = limit;
    
    def compute(self, a, b, naive = False):
        """ Computation of multiplication """
        try:
            for i in range(self.limit - len(a)): a.append(0)
            for i in range(self.limit - len(b)): b.append(0)
              
            c = self.multiply_naive(a, b) if naive else self.multiply(a, b) 

            return self.to_string(self.carry(c))

        except Exception as e:
            raise

    def multiply_naive(self, a, b):
        """ Naive multiplication. """
        try:
            a_len, b_len = len(a), len(b)
          
            z = [0 for _ in range(a_len + b_len)]
          
            for j in range(b_len):
                for i in range(a_len):
                    z[j + i] += a[i] * b[j]

            return z
        except Exception as e:
            raise

    def multiply(self, a, b):
        """ Toom-Cook implementation. """
        
        a_0, a_1, a_m1, a_m2, a_inf = [], [], [], [], []
        b_0, b_1, b_m1, b_m2, b_inf = [], [], [], [], []
        c_0, c_1, c_m1, c_m2, c_inf = [], [], [], [], []

        r0, r1, r2, r3, r4          = [], [], [], [], []
        
        try:
            length = len(a)
            if length <= 9: return self.multiply_naive(a, b)
            
            # ----------====== Splitting ======----------
            
            # P(x) = a2 * x^2 + a1 * x + a0
            a2 = a[(length * 2 // 3):                 ]
            a1 = a[  (length // 3)  :(length * 2 // 3)]
            a0 = a[                 :  (length // 3)  ]
            
            # Q(x) = b2 * x^2 + b1 * x + b0
            b2 = b[(length * 2 // 3):                 ]
            b1 = b[  (length // 3)  :(length * 2 // 3)]
            b0 = b[                 :  (length // 3)  ]
            
            # --------====== Evaluation ======----------
            
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
            
            # -----=== Pointwise multiplication ===-----
            
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
                        
            # --------===== Interpolation =====--------
            
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
                
            # -----=== Calculating final number ===-----

            # ==== z = r4 * x^4 + r3 * x^3 + r2 * x^2 + r1 * x + r0
            z = r0 + r2 + r4
            for i in range((length // 3) * 2): z[i + length // 3]     += r1[i]
            for i in range((length // 3) * 2): z[i + length // 3 * 3] += r3[i]
                
            return z
            
        except Exception as e:
            raise


    def carry(self, z):
        """ Implements algorithm of carrying. """
        c = 0
        try:
            for i in range(len(z)):
                z[i] += c
                c = z[i] // 10  
                z[i] -= c * 10
        
            if c != 0:
                print("Seems like overflow. Check maximum possible number of digits", cr)
            return z
        except Exception as e:
            raise

    def to_string(self, x):
        """ Converts a reversed array to string, which represents a number. """
        n = len(x)
        try:
            while x[n - 1] == 0: n -= 1
            return ''.join(str(x[i]) for i in range(n - 1, -1, -1))
        except Exception as e:
            raise

    def to_array(self, str):
        """ Generates a reversed array of digits from string. """
        if (len(str) > self.limit):
            print("Number is bigger than limit")
            return

        return [int(i) for i in reversed(str)]