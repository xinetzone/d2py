def fib(n):
    '''打印斐波那契数列，直至 n'''
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()


def fib2(n):
    '''返回斐波那契数列，直至 n'''
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result


if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
