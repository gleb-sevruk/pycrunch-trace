from time import sleep


def function_call(**kwargs):
    print(kwargs)
    sleep(0.1)
    sum = kwargs['a'] + kwargs['b']
    return sum


def show_me_how_to_navigate_using_graph():
    print('Lets say we have a function call')
    function_call(a=1, b=2)
    sleep(0.12)

    print('Clicking on function in a graph panel')
    print('  brings you to the beginning of the method')

    print('  Holding Shift and click will navigate you to the END')
    print('    So you can overview return values and state of locals')
    print('    Right before exiting from the method')

    print('You can step out of any function by Shift + Down Arrow')
    return 42

