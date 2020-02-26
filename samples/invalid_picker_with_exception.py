import pickle
import sys

def op():
    try:
        x = pickle.dumps(dict(a=1,b='11'))
        x = pickle.dumps(sys)
    except Exception as e:
        sss = str(e)
        pass
