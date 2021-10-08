from random import randint
import copy


def num_process(num_str):  # from string to list
    num = []
    for c in num_str:
        num.append(int(c))
    return num


def x_add(num1, num2, carry, x_sum):  # add two numbers
    if num1 == [] or num2 == []:
        if carry == 0:
            x_sum = num2 + x_sum if num1 == [] \
                else num1 + x_sum
            while x_sum[0] == 0:
                x_sum.pop(0)
                if x_sum == []:
                    x_sum = [0]
                    break
            if x_sum[0] > 0:
                ef = 1
            else:
                ef = -1
            for i in range(len(x_sum)-1, 0, -1):
                if x_sum[i] * ef < 0:
                    x_sum[i - 1] -= ef
                    x_sum[i] += 10 * ef
            while x_sum[0] == 0:
                x_sum.pop(0)
                if x_sum == []:
                    x_sum = [0]
                    break
            return x_sum
        return x_add([0], num2, carry, x_sum) if num1 == [] \
            else x_add(num1, [0], carry, x_sum)

    decimal_sum = num1.pop() + num2.pop() + carry
    carry = 0
    if -10 < decimal_sum < 10:
        x_sum = [decimal_sum] + x_sum
    else:
        carry = int(decimal_sum / 10)
        decimal_sum -= carry * 10
        x_sum = [decimal_sum] + x_sum

    return x_add(num1, num2, carry, x_sum)


def rsa_add(num1, num2, modulo):  # add two numbers (mod modulo)
    v1 = copy.deepcopy(num1)
    v2 = copy.deepcopy(num2)
    if modulo == []:
        return x_add(v1, v2, 0, [])
    m = copy.deepcopy(modulo)
    sum_m = x_add(v1, v2, 0, [])
    sum_m_r = sum_m
    if sum_m[0] > 0:  # positive sum
        neg_m = [-e for e in m]
        while True:
            sum_m_r = x_add(copy.deepcopy(sum_m_r),
                            copy.deepcopy(neg_m), 0, [])
            if sum_m_r[0] < 0:
                break
            else:
                sum_m = sum_m_r
    else:  # negative sum
        while True:
            sum_m_r = x_add(copy.deepcopy(sum_m_r),
                            copy.deepcopy(m), 0, [])
            if sum_m_r[0] > 0:
                sum_m = sum_m_r
                break
    return sum_m


def x_mul(num1, num2, modulo):  # multiply two numbers
    if num1 == []:
        return [0]
    x_sum = [0]
    p = num1.pop()
    for i in range(p):
        x_sum = rsa_add(x_sum, num2, modulo)
    x_sum_r = x_mul(num1, num2, modulo)
    x_sum_r_10 = [0]
    for i in range(10):
        x_sum_r_10 = rsa_add(x_sum_r_10, x_sum_r, modulo)
    return rsa_add(x_sum, x_sum_r_10, modulo)


def rsa_mul(num1, num2, modulo):  # multiply two numbers (mod modulo)
    v1 = copy.deepcopy(num1)
    v2 = copy.deepcopy(num2)
    m = copy.deepcopy(modulo)
    if v1[0] < 0:
        v1 = [-e for e in v1]
    if v2[0] < 0:
        v2 = [-e for e in v2]
    x_sum = x_mul(v1, v2, m)
    if num1[0] * num2[0] < 0:
        x_sum = [-e for e in x_sum]
    return x_sum


def x_pow(xb, xp, m):  # xb to the power of xp (mod m)
    if xp == []:
        return [1]
    x_sum = [1]
    p = xp.pop()
    for i in range(p):
        x_sum = rsa_mul(x_sum, xb, m)
    x_sum_r = x_pow(xb, xp, m)
    x_sum_r_10 = [1]
    for i in range(10):
        x_sum_r_10 = rsa_mul(x_sum_r_10, x_sum_r, m)
    return rsa_mul(x_sum, x_sum_r_10, m)


def rsa_pow(xb, xp, modulo):  # xb to the power of xp (mod modulo)
    xb0 = copy.deepcopy(xb)
    xp0 = copy.deepcopy(xp)
    m = copy.deepcopy(modulo)
    x_sum = x_pow(xb0, xp0, m)
    return x_sum


def rsa_extended_gcd(v1, v2):  # extended Euclidean
    # assuming v1 > v2
    a = copy.deepcopy(v1)
    b = copy.deepcopy(v2)
    q = [0]
    a_r = a
    neg_b = [-e for e in b]
    r = []
    while True:
        a_r = rsa_add(copy.deepcopy(a_r),
                      copy.deepcopy(neg_b), [])
        if a_r[0] < 0:
            break
        else:
            q = rsa_add(copy.deepcopy(q), [1], [])
            r = a_r
    if r == [0]:
        return [0], [1]
    x, y = rsa_extended_gcd(copy.deepcopy(b),
                            copy.deepcopy(r))
    # x: previous coefficient of a
    # y: previous coefficient of b
    yq = rsa_mul(copy.deepcopy(y),
                 copy.deepcopy(q), [])
    neg_yq = [-e for e in yq]
    return y, rsa_add(copy.deepcopy(x),
                      copy.deepcopy(neg_yq), [])


def rsa_inverse(v, modulo):  # the inverse of v (mod modulo)
    a = copy.deepcopy(v)
    m = copy.deepcopy(modulo)
    x, y = rsa_extended_gcd(m, a)
    inv = rsa_add(copy.deepcopy(y), [0], m)
    return inv


def sign(M, n, d):
    signature = rsa_pow(M, d, n)
    return signature


def verify(S, n, e, M):
    M_ = rsa_pow(S, e, n)
    v = True if M_ == M else False
    return v


def blindsign(M, n, e, d):
    r = []
    for i in range(len(n)):
        r_i = randint(0, n)
        r.append(r_i)
    Mb = rsa_mul(rsa_pow(r, e, n), M, n)
    Sb = sign(Mb, n, d)
    S = rsa_mul(rsa_inverse(r, n), Sb, n)
    Mb = rsa_mul(rsa_pow(r, e, n), M, n)
    Sb = sign(Mb, n, d)
    S = rsa_mul(rsa_inverse(r, n), Sb, n)
    return S


if __name__ == '__main__':
    M_str = "16410"
    n_str = "17399"
    e_str = "5"
    d_str = "13709"

    M = num_process(M_str)
    n = num_process(n_str)
    e = num_process(e_str)
    d = num_process(d_str)

    S = sign(M, n, d)
    V = verify(S, n, e, M)
    S_ = blindsign(M, n, e, d)
    Vb = verify(S_, n, e, M)

    S_str = ""
    for i in S:
        S_str += str(i)
    print("S =", S_str)
    print("V =", V)

    S__str = ""
    for i in S_:
        S__str += str(i)
    print("S_ =", S__str)
    print("Vb =", Vb)
