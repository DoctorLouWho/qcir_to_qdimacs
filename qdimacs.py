###############################################
#       
#       code is still incomplete
# *need to fix num of clauses
#           qcir to qdimacs
###############################################

import re
import sys

orig_stdout = sys.stdout

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
        self.out_f = open('outi.qcir', 'w')
        self.trans_vars = {}
        self.max = 0
        self.exist_list = []
        self.init_var = []
        self.and_list = []
        self.print_list = []

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
            print('{} {} 0'.format('-'+x, a).replace('--',''))
            temp += '-{} '.format(a)
        
        self.trans_vars[v] = x
        
        print('{} {} 0'.format(x, temp[:-1]).replace('--',''))
        self.and_list.extend([str(self.max-i) for i in range(len(line_list)-2,-1,-1)])
        # print()
        
    def expand_or(self, line_list):
        temp = ''
        x = str(self.mxi())
        self.exist_list.append(x)
        v = line_list[0]
        for a in line_list[2:]:
            if a in self.trans_vars:
                a = self.trans_vars[a]
            print('{} {} 0'.format(x, '-'+a).replace('--',''))
            temp += '{} '.format(a)

        self.trans_vars[v] = x
    
        print('{} {} 0'.format('-'+x, temp[:-1]).replace('--',''))
        self.and_list.extend([str(self.max-i) for i in range(len(line_list)-2,-1,-1)])
        # print()
        
    def process_line(self, line):
        """ processes each line, calls to expand_and or expand_or 
        """
        line = line.strip()
        line = line.split('#')[0]
        
        if not line:
            return
        
        # print('#' + line)

        line_list = [i for i in re.split("[=(),\s]", line) if i]
        

        if line_list[0] == 'exists':
            #flush 
            # self.exist_list = []
            # self.exist_list += line_list[1:]
            self.print_list.append('e {} '.format(' '.join(line_list[1:])))

        if line_list[0] == 'forall': 
            self.print_list.append('a {} '.format(' '.join(line_list[1:])))

        if 'and' in line_list:
            self.expand_and(line_list)

        elif 'or' in line_list:
            self.expand_or(line_list)

        if line_list[0].isnumeric():
            self.init_var.append(line_list[0])

    def file_reader(self):
        """ reads each line, returns file ptr and max num
        """
        sys.stdout = self.out_f
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
        
        print(self.exist_list[-1], 0)
        self.out_f.close()

        if 'e' in self.print_list[-1]:
            self.print_list[-1] += ' '.join(self.exist_list) + ' 0'
        else:
            self.print_list.append('e {} 0'.format(' '.join(self.exist_list)))

        line_prepender('outi.qcir', '0 \n'.join(self.print_list))
        line_prepender('outi.qcir', 'p cnf {} {}'.format(self.exist_list[-1], len(self.init_var)*3+1))

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