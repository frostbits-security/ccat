# library with different useful functions to use them within various modules

# converts string list of numbers to list of ints with those numbers
# ['1','2','3'] -> [1,2,3]
def intify(strlist):
    res=[]
    for i in strlist:
        res.append(int(i))
    return res

#Add value to the feature interface_dict

def int_dict_parse(parse_meth,featur_str,name,featur_dict):

    value = parse_meth.parseString(featur_str).asList()
    featur_dict[name] = value
    return featur_dict
