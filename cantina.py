import json
import pandas as pd
from pandas.io.json import json_normalize

"""
Note:
    - the script assumes SystemViewController.json resides in the same location
      as the script itself
    - you may enter class, class names, or identifiers verbatim
      e.g. Input, accessoryView, windowMode
"""

def rec_parse(obj, selector):
    
    vec = []
    holder = []
    
    def find_selector(obj, vec, selector):
        
        if isinstance(obj, dict):
            holder.append(obj)
            for k,v in obj.iteritems():
                
                if k == selector:
                    vec.append(obj)
                    find_selector(v, vec, selector)
                elif v == selector:
                    vec.append(obj)
                    find_selector(v, vec, selector)
                elif isinstance(v, (dict,list)):
                    holder.append(obj)
                    find_selector(v, vec, selector)
        
        elif isinstance(obj, list):
            for item in obj:
                if item == selector:
                    vec.append(holder[len(holder)-1])
                find_selector(item, vec, selector)
        
        return vec
    
    views = find_selector(obj, vec, selector)
    return views

def format_output(views, selector):
    
    for view in views:
        viewdf = json_normalize(view)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print viewdf
            print '\n'

    return

if __name__ == '__main__':
    

    with open('SystemViewController.json') as obj:
        data = json.load(obj)
        
    prompt = 'please enter a class, class name, or identifier: \n'
    
    while True:
        
        selector = raw_input(prompt)
        if len(selector) == 0: 
            break
        else:
            print '\n'
            views = rec_parse(data, selector)
            format_output(views, selector)
    
    