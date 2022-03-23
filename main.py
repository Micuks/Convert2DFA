import json, argparse

class nfa:
    def __init__(self, model):
        self.states = model['states']
        self.alphabet = model['alphabet']
        self.delta_function = model['delta function']
        self.initial_state = model['initial state']
        self.terminal_states = model['terminal states']
    def raw(self):
        __tmpdict = dict()
        __tmpdict['states'] = self.states
        __tmpdict['alphabet'] = self.alphabet
        __tmpdict['delta function'] = self.delta_function
        __tmpdict['initial state'] = self.initial_state
        __tmpdict['terminal states'] = self.terminal_states
        return __tmpdict

class dfa(nfa):
    def __init__(self, model):
        nfa.__init__(self, model)
    def raw(self):
        return nfa.raw(self)

def modellist(filename):
    ''' Read NFAs from given file. '''
    content = json.load(open(filename, "r", encoding="utf-8"))
    model = content['nfa items']
    tmplist = list()
    for item in model:
        tmplist.append(item)
    return tmplist

def powerset(superset):
    ''' Get all subsets of the given set. '''
    subsets = list()
    for i in range(2**len(superset)):
        subset = list()
        for j in range(len(superset)):
            if 1<<j & i != 0:
                subset.append(superset[j])
        subset.sort()
        subsets.append(subset)
    #pprint(subsets)
    return subsets

def convert2dfa(dict_nfa):
    ''' Convert NFA to DFA '''
    tmp_dfa = dfa(dict_nfa)
    tmp_dfa.states = powerset(tmp_dfa.states)

    tmp_delta_function = dict()
    for alpha in tmp_dfa.delta_function:
        tmp_delta_function[alpha] = dict()
        tmpset = set()
        for beta in tmp_dfa.states:
            if len(beta) == 0:
                continue
            tmpset.clear()
            for gamma in beta:
                if gamma in tmp_dfa.delta_function[alpha]:
                    for item in tmp_dfa.delta_function[alpha][gamma]:
                        tmpset.add(item)
            listset = list(tmpset)
            listset.sort()
            tmp_delta_function[alpha][str(beta)] = listset
    tmp_dfa.delta_function = tmp_delta_function
    terminal_set = set()
    for item in tmp_dfa.states:
        if not set(tmp_dfa.terminal_states).isdisjoint(set(item)):
            terminal_set.add(str(item))
    tmp_dfa.terminal_states = list(terminal_set)
    return tmp_dfa

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert NFA to DFA. From console or selected json file.")
    parser.add_argument("-f", "--file", help="Convert from the given file. It can contain more than one DFAs.", type=str)
    parser.add_argument("-d", "--destination", help="Output to given file.", type=str)
    args = parser.parse_args()
    list_dfa = list()
    if args.file:
        for item in modellist(args.file):
            item_nfa = nfa(item)
            list_dfa.append(convert2dfa(item_nfa.raw()))
    else:
        input_nfa = nfa(dict())
        input_nfa.states = input("Please input NFA states.")

    if args.destination:
        fp = open(args.destination, "w", encoding="utf-8")
        dict_dfa = dict()
        dict_dfa['dfa items'] = list()
        for item in list_dfa:
            dict_dfa['dfa items'].append(item.raw())
        json.dump(dict_dfa, fp, indent=4)
        fp.close()
    else:
        for item in list_dfa:
            print(json.dumps(item.raw(), indent=4))
#    for item in modellist("./nfa.json"):
#        fp = open("./dfa.json", "w", encoding="utf-8")
#        fp.write(json.dumps(output_dfa.raw(), indent=4))
