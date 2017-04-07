# Jackie's Universal Cartographics System Code Decoder
# Kay Johnston
# Now with added elegance.  And fixed the silly muppet bug I introduced merging things.  :)

# Reference
# High points, below plane
# KF-D C29, PG-D C29
# QW-F C, VX-F C
# Low points, above plane
# UI-X C28, ZJ-X C28
# AA-A C, FB-A C
# High points, below plane
# EK-C D14, TK-C D14
# WV-C D, LW-C D
# Low points, above plane
# IO-Z D13, XO-Z D13
# AA-A D, PA-A D

# Add brute force systems-near-system finder.

# v4 for EAFOTS search

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

divisor = 26
middle = divisor**2
biggest = divisor**3
# Can merge these.
masscodes = 'HGFEDCBA'
sectorlength = 1280
sidelength = 128
walllength = 128 * 128

def cubes():
    short_alpha = 'HGFEDCBA'
    cubeside = 1280
    for letter in short_alpha:
        print(letter,':',cubeside,' lightyear sides, which is',int(1280/cubeside),'subsectors.')
        cubeside = int(cubeside/2)

def finder(column,row,stack):
    position = 0
    position += row * walllength
    position += stack * sidelength
    position += column

    #print('column:',column,'row:',row,'stack:',stack,'gives position:',position)

    number = int(position / biggest)
    working = position - (number * biggest)

    number_third = int(working / middle)
    third = alphabet[number_third]
    working = working - (number_third * middle)

    number_second = int(working / divisor)
    second = alphabet[number_second]
    working = working - (number_second * divisor)
    
    first = alphabet[working]

    if number != 0:
        text = first + second + '-' + third + ' (letter code)' + str(number) + '-(system code)'
    else:
        text = first + second + '-' + third + ' (letter code)(system code)'
        
    #print(text)
    return first,second,third,number

class System():

    def __init__(self,first,second,third,masscode,n1,n2):
        try:
            self.first = first.upper()
            self.second = second.upper()
            self.third = third.upper()
            self.masscode = masscode.upper()
            self.n1 = int(n1)
            self.n2 = int(n2)
        except:
            print('There\'s a problem with those values.')
        # Could add extra error checking here.
        self.name = self.first + self.second + '-' + self.third + ' ' + self.masscode
        if self.n1 == 0:
            self.name += str(self.n2)
        else:
            self.name += str(self.n1) + '-' + str(self.n2)
        self.calculate()

    def calculate(self):
        # Change the index into decimal.
        self.index = 0
        self.index += alphabet.index(self.first)
        self.index += alphabet.index(self.second) * 26
        self.index += alphabet.index(self.third) * 26 * 26
        self.index += self.n1 * 26 * 26 * 26
        # Work out the position of this index in slices, rows and columns.
        self.rows = int(self.index / walllength)
        remainder = self.index - (self.rows * walllength)
        self.slices = int(remainder / sidelength)
        self.columns = remainder - (self.slices * sidelength)
        # Get an approximate position given the masscode.
        self.divisions = 2**(masscodes.index(self.masscode))
        self.sidelength = int(sectorlength / self.divisions)
        self.x = int(self.columns * self.sidelength) + int(self.sidelength/2)
        self.y = int(self.rows * self.sidelength) + int(self.sidelength/2)
        self.z = int(self.slices * self.sidelength) + int(self.sidelength/2)
        
    def report(self):
        print(self.name)
        print('Column:',self.columns,'Row:',self.rows,'Slice:',self.slices)
        print('X: ~',self.x,'Y: ~',self.y,'Z: ~',self.z)
        print()

def bruteforce(target,radius):
    print(target.columns,target.rows,target.slices)
    print(target.x,target.y,target.z)

def getsubs(x,y,z):
    # Boxel size equivalent to E mass code subsector.
    subsector_list = []
    # E
    first,second,third,number = finder(x,y,z)
    newsystem = System(first,second,third,'E',number,0)
    subsector_list.append(newsystem)
    # D
    startx = x * 2
    starty = y * 2
    startz = z * 2
    endx = ((x + 1) * 2)# - 1
    endy = ((y + 1) * 2)# - 1
    endz = ((z + 1) * 2)# - 1
    for sx in range(startx,endx):
        for sy in range(starty,endy):
            for sz in range(startz,endz):
                first,second,third,number = finder(sx,sy,sz)
                newsystem = System(first,second,third,'D',number,0)
                subsector_list.append(newsystem)
    # C
    startx = x * 4
    starty = y * 4
    startz = z * 4
    endx = ((x + 1) * 4)# - 1
    endy = ((y + 1) * 4)# - 1
    endz = ((z + 1) * 4)# - 1
    for sx in range(startx,endx):
        for sy in range(starty,endy):
            for sz in range(startz,endz):
                first,second,third,number = finder(sx,sy,sz)
                newsystem = System(first,second,third,'C',number,0)
                subsector_list.append(newsystem)
    # B
    startx = x * 8
    starty = y * 8
    startz = z * 8
    endx = ((x + 1) * 8)# - 1
    endy = ((y + 1) * 8)# - 1
    endz = ((z + 1) * 8)# - 1
    for sx in range(startx,endx):
        for sy in range(starty,endy):
            for sz in range(startz,endz):
                first,second,third,number = finder(sx,sy,sz)
                newsystem = System(first,second,third,'B',number,0)
                subsector_list.append(newsystem)
    # A
    startx = x * 16
    starty = y * 16
    startz = z * 16
    endx = ((x + 1) * 16)# - 1
    endy = ((y + 1) * 16)# - 1
    endz = ((z + 1) * 16)# - 1
    for sx in range(startx,endx):
        for sy in range(starty,endy):
            for sz in range(startz,endz):
                first,second,third,number = finder(sx,sy,sz)
                newsystem = System(first,second,third,'A',number,0)
                subsector_list.append(newsystem)
    # Finish
    return subsector_list

def writelist(subsector_list,filename):
    with open(filename,'w') as opened:
        opened.write('SECTOR,FIRST,SECOND,THIRD,MASSCODE,N1,N2\n')
        for thing in subsector_list:
            opened.write('EAFOTS,')
            opened.write(thing.first)
            opened.write(',')
            opened.write(thing.second)
            opened.write(',')
            opened.write(thing.third)
            opened.write(',')
            opened.write(thing.masscode)
            opened.write(',')
            opened.write(str(thing.n1))
            opened.write(',')
            opened.write(str(thing.n2))
            opened.write('\n')

cubes()
print()

Alice = System('I','Q','Y','D',0,0)
Alice.report()

alice = getsubs(0,0,0)


##print('Started.')
##for x in range(0,8):
##    for y in range(0,8):
##        for z in range(0,8):
##            alice = getsubs(x,y,z)
##            filename = 'EAFOTS' + str(x) + ',' + str(y) + ',' + str(z) + '.csv'
##            writelist(alice,filename)
##print('Finished')

##bruteforce(Alice,10)

##x = input('Please enter the x co-ordinate for the mass-code E boxel: ')
##y = input('Please enter the y co-ordinate for the mass-code E boxel: ')
##z = input('Please enter the z co-ordinate for the mass-code E boxel: ')
##
##filename = 'EAFOTS' + x + ',' + y + ',' + z + '.csv'
##
##alice = getsubs(int(x),int(y),int(z))
##
##writelist(alice,filename)



##finder(0,0,0)
##finder(0,1,0)
##finder(0,2,0)
##finder(0,3,0)
##finder(0,0,1)
