# from pycrunch_trace.events.size_prediction import SizeBreakdown


# @pytest.mark.skip()
# def test_1():
#     x = SizeBreakdown.load_from_session()
import random
import string

from pycrunch.insights import trace

from pycrunch_trace.file_system.human_readable_size import HumanReadableByteSize


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Repeat(object):
    def __init__(self, times):
        self.times = times

    def  __str__(self):
        res =  ''
        for i in range(self.times):
            res += '/' + randomString(20)
        return res


def random_filename():
    return 'users/' + randomString(5) + '/projects/' + randomString(20) + '/' + randomString(20) + Repeat(random.randint(1, 6)).__str__() + '.py'


class NewEvent:
    event_names = ['method_enter', 'line', 'method_exit']

    def __init__(self, filename):
        self.name = random.choice(OldEvent.event_names)
        self.line = random.randint(1, 1000)
        self.filename = filename
        self.function_name = randomString(random.randint(1,20))

    def size(self):
        function_name_size = len(self.function_name)

        call_stack_length = 8 + 8 + 8 + function_name_size + 8
        method_name_size = len(self.name)
        method_name_size = 0
        return call_stack_length + method_name_size + 8 + 8 + function_name_size


class OldEvent:
    event_names = ['method_enter', 'line', 'method_exit']

    def __init__(self, filename):
        self.name = random.choice(OldEvent.event_names)
        self.line = random.randint(1, 1000)
        self.filename = filename
        self.function_name = randomString(random.randint(1,20))

    def size(self):
        call_stack_length = 8 + 8 + len(self.name) + len(self.filename)
        return call_stack_length + len(self.name) + 8 + len(self.filename) + len(self.function_name)

def test_old_size():
    total_files = 255
    files_in_session = []
    for x in range(total_files):
        files_in_session.append(random_filename())
    # trace(files_in_session=files_in_session)
    total = 0
    for x in range(10000):
        total += size_of_random_event(files_in_session)
    # 10000 ='3.2 MB'
    # 100000 = 31 MB
    # 1 000 000 = 310 MB
    str__ = HumanReadableByteSize(total).__str__()
    print(str__)
    trace(total=str__)

def test_new_size():
    total_files = 255
    files_in_session = []
    size_files = 0
    for x in range(total_files):

        filename = random_filename()
        size_files += len(files_in_session)
        files_in_session.append(filename)

    trace(size_files=size_files)

    # trace(files_in_session=files_in_session)
    total = 0
    for x in range(10000):
        total += size_of_new_random_event(files_in_session)
    # 10000 ='3.2 MB'
    # 100000 = 31 MB
    # 1 000 000 = 310 MB
    str__ = HumanReadableByteSize(total).__str__()
    print(str__)
    trace(total=str__)

def size_of_random_event(files_in_session):
    return OldEvent(random.choice(files_in_session)).size()

def size_of_new_random_event(files_in_session):
    return NewEvent(random.choice(files_in_session)).size()

def test_232():
    print('s')