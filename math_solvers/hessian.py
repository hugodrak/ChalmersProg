import sympy
import itertools


def hessian(func, **at):
    """
        Calculates hessian matrix for function
    :param func: sympy-function
    :param at: optional key-values pairs with values of symbol-value at the point of evaluation. If not provided
                performs generic differentiation
    """
    variables = sorted(func.free_symbols, key=lambda x: x.name)
    num_variables = len(variables)
    print('Hessian')
    print(f'variables are: {variables}')

    result_matrix = sympy.zeros(num_variables, num_variables)

    # Itertools is awesome!
    for with_respect_to, indices in zip(itertools.product(variables, repeat=2),
                                        itertools.product(range(num_variables), repeat=2)):

        differentiated = func.diff(*with_respect_to)
        for variable, value in at.items():
            differentiated = differentiated.subs(variable, value)

        result_matrix[indices[0], indices[1]] = differentiated

    sympy.pprint(result_matrix)
    print('Eigenvalues')
    for eigenvalue in result_matrix.eigenvals():
        sympy.pprint(eigenvalue)


def test_hessian():
    x, y = sympy.symbols('x y')

    #func = x * sympy.exp(-x ** 3 + y ** 3)
    hessian(func)
    hessian(func, x=sympy.Rational(1, sympy.root(3, 3)), y=0)


def temp():
    x, y = sympy.symbols('x y')

    func = x * sympy.exp(-sympy.Pow(x, 3) + sympy.Pow(y, 3))
    func.subs(x=sympy.Rational(1, sympy.root(3, 3)), y=0)


if __name__ == '__main__':
    sympy.init_printing(use_unicode=True)
    temp()
    # test_hessian()
