import sys
import traceback

def get_error_string(e, tb=True):
    ex_type, ex_value, ex_traceback = sys.exc_info()
    if tb:
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    text = "Exception type : %s " % ex_type.__name__
    text += "\nException message : %s" % ex_value
    if tb:
        text += "\n".join(stack_trace)
    return text
