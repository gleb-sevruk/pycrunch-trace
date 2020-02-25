class GlebTracer:
    def __init__(self):
        self.current_filename = None
        pass

    def trace_calls_and_returns(self, frame, event, arg):
        filename_to_log = ''
        if self.current_filename != frame.f_code.co_filename:
            self.current_filename = frame.f_code.co_filename
            filename_to_log = self.current_filename

        print(f': {filename_to_log}:{frame.f_lineno} {event}')

        co = frame.f_code
        func_name = co.co_name
        if func_name == 'write':
            # Ignore write() calls from printing
            return
        line_no = frame.f_lineno
        filename = co.co_filename
        blacklisted = self.is_blacklisted(filename)
        if blacklisted:
            # Ignore calls not in this module
            return
        if event == 'call':
            print('* Call to function `{}` located on line {} of {}'.format(
                func_name, line_no, filename))
            return self.trace_calls_and_returns
        elif event == 'return':
            print('* return:event -> function `{}` => return value: `{}`'.format(func_name, arg))
        return

    def is_blacklisted(self, filename):
        # endswith = filename.endswith('sys_settrace_return.py')
        return False