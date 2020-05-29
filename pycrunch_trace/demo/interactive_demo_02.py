from time import sleep


def method_in_another_file(some_number: int):
    print('File contents are stored as they were at the moment of the recording.')

    print('For easy navigation, press G to open graph panel')
    print('Graph will give overview of method calls and their approximate duration.')

    print('Check this:')
    sleep(0.15)

    print('You can see on the graph that we are at 150ms mark of the recording.')
    print('Current time (since recording start) is also displayed in inspector')
    print('  And on graph panel as a needle')

    print('You can skip next method call by using Down Arrow [↓]')
    print('Or enter into by Right Arrow [→]')
    dummy_method()

    print('Note __return pseudo-variable as we exit from this method')
    return some_number * 3 + 1


def dummy_method():
    print('See how `index` variable is changed as you step through the loop')
    for index in range(5):
        print('If you got trapped in a loop like this, use Shift+Down Arrow to step out of this method')
        print('You can also try Shift+Up Arrow to get to the place where this method was called')
        sleep(0.03)

    # if you are not able to read all text, you can toggle inspector
    #   by pressing [i]
