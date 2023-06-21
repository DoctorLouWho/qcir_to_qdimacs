###############################################
#
#       code is still incomplete
#
#   normal qcir conversion to cnf format qcir 
#
###############################################

import re
import sys

orig_stdout = sys.stdout
f = open('out.qcir', 'w')

def line_prepender(filename, line):
    """ append line to begining of file 
    """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

###############################################################################
class solve():

    def __init__(self, file_name):
        self.fp = open(file_name, 'r')
        # self.out_f = open('out.qcir', 'w')
        self.trans_vars = {}
        self.max = 0
        self.exist_list = []
        self.init_var = []

    def mxi(self):
        self.max += 1
        return self.max

    def expand_and(self, line_list):
        temp = ''
        x = str(self.mxi())
        self.exist_list.append(x)
        v = line_list[0]
        for a in line_list[2:]:
            if a in self.trans_vars:
                a = self.trans_vars[a]
            print('{} = or({},{})'.format(str(self.mxi()) , '-'+x, a).replace('--',''))
            temp += '-{},'.format(a)
        
        self.trans_vars[v] = x
        
        print('{} = or({},{})'.format(str(self.mxi()), x, temp[:-1]).replace('--',''))
        print('{} = and({})'.format(v , ','.join([str(self.max-i) for i in range(len(line_list)-2,-1,-1)])))
        print()
        
    def expand_or(self, line_list):
        temp = ''
        x = str(self.mxi())
        self.exist_list.append(x)
        v = line_list[0]
        for a in line_list[2:]:
            if a in self.trans_vars:
                a = self.trans_vars[a]
            print('{} = or({},{})'.format(str(self.mxi()) , x, '-'+a).replace('--',''))
            temp += '{},'.format(a)

        self.trans_vars[v] = x
    
        print('{} = or({},{})'.format(str(self.mxi()), '-'+x, temp[:-1]).replace('--',''))
        print('{} = and({})'.format(v , ','.join([str(self.max-i) for i in range(len(line_list)-2,-1,-1)])))
        print()
        
    def process_line(self, line):
        """ processes each line, calls to expand_and or expand_or 
        """
        line = line.strip()
        line = line.split('#')[0]
        
        if not line:
            return
        
        print('#' + line)
        line_list = [i for i in re.split("[=(),\s]", line) if i]
        

        if line_list[0] == 'exists':
            #flush 
            self.exist_list = []
            self.exist_list += line_list[1:]

        if 'and' in line_list:
            self.expand_and(line_list)

        elif 'or' in line_list:
            self.expand_or(line_list)

        if line_list[0].isnumeric():
            self.init_var.append(line_list[0])

    def file_reader(self):
        """ reads each line, returns file ptr and max num
        """
        sys.stdout = f
        x = ''
        for line in self.fp:
            line = line.strip()

            if line[0] == '#':
                continue
            
            # # print(re.split('\W+', line, 0))
            # print([i for i in re.split("[=(),\s]", line) if i])

            #find max num in line
            new_max = max([int(i) for i in re.split('\W+', line, 0) if i.isnumeric()])
            self.max = max(new_max, self.max)

                
        self.fp.seek(0)

        for line in self.fp:
            self.process_line(line)
        
        print(','.join(self.init_var[:-1]) + ',' +self.exist_list[-1])
        f.close()

        line_prepender('out.qcir', 'exists({})'.format(','.join(self.exist_list)))
        

        return
    
###############################################################################
def main():
    file_name = input("Please insert a file name: ")
    
    # sys.stdout = f

    sil = solve(file_name)
    sil.file_reader()

    sys.stdout = orig_stdout
    
    # f.close()
    
if __name__ == "__main__": 
    main()