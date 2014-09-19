import os
import datetime
import re

'''
Created on 2014 May 20
@author: Gautier
'''


class ParseView():
    '''
    class parsing the view to dal and dalwrapper
    '''
    def __init__(self):
        self.views = []
       
            
    def parseFile(self, myfile):
        f = open(myfile,'r')
        fromTable = re.compile('.*FROM ([A-Z_]+)', re.IGNORECASE)
        viewname = re.compile('create view \[([A-Z_]+)\] as', re.IGNORECASE)
        viewclasses = re.compile('.* JOIN ([A-Z_]+) .* .* ON .*', re.IGNORECASE)
        viewclasses2 = re.compile('.* JOIN ([A-Z_]+) ON .*', re.IGNORECASE)
        for line in f:
            viewname_ = viewname.match(line)
            if viewname_ is not None:
                print('###'+viewname_.group(1))
                self.views.append(View())
                self.views[len(self.views)-1].setName(viewname_.group(1))

            fromTable_ = fromTable.match(line)
            if fromTable_ is not None:
                print('~'+fromTable_.group(1))
                self.views[len(self.views)-1].addtable(fromTable_.group(1))
            
            viewclasses_ =  viewclasses.match(line)
           
            if viewclasses_ is not None:
                g = viewclasses_.group(1)
                print('-'+g)
                self.views[len(self.views)-1].addtable(g)
            else :
                viewclasses_ =  viewclasses2.match(line)
                
                if viewclasses_ is not None:
                    for g in viewclasses_.groups():
                        print('--'+g)
                        self.views[len(self.views)-1].addtable(g)
                    

    def createDalsView(self):
        for view in self.views:
            self.writeToFile(view.createDalView(),view.name+'DalWrapper.java')
            

    def writeToFile(self,content,filename):
        baseFileDIR = 'viewsWrapper'
        if not os.path.exists(baseFileDIR):
            os.makedirs(baseFileDIR)
        out = open(baseFileDIR+'/'+filename,'w')
        out.write(content)
        print("..."+filename+" created")
        
                
    def __repr__(self):
        for view in self.views:
            print('-------------\n')
            print(str(view))
            
            
    def __str__(self):
        for view in self.views:
            print('-------------\n')
            print(str(view))
            

            


class View():

    def __init__(self):
        self.classes = []

    def setName(self,name):
        self.name = name

    def addtable(self,table):
        self.classes.append(table)

    def createDalView(self):
        result = 'package com.kayentis.epro.sqlite.views.wrapper;\n\n'
        result += 'import android.database.Cursor;'
        result += 'import com.kayentis.epro.sqlite.cursor.*;\n'
        result += 'import com.kayentis.epro.sqlite.dal.*;'
        result += 'import com.kayentis.epro.sqlite.dal.wrapper.*;\n\n'
        result += 'public class '+self.name+'DalWrapper {\n \n'
        result += ''
        for attr in self.classes:
            result += '   private '+attr+' '+attr[0].lower()+attr[1:]+';\n'
        result += '\n'
        start = '0'
        for attr in self.classes:
            result += '   public static '+attr+' get'+attr+'(Cursor cursor) {\n'
            result += '      int start='+start+';\n'
            start += '+\n      '+attr+'DalWrapper.getNbColumns()'
            result += '      return '+attr+'DalWrapper.getObjectFromDB(new '+attr+'Cursor(cursor), start);'
            result += '\n   }\n \n'
        result += '}\n'
        result += ''
        result += ''
        return result

    def __repr__(self):
        result = self.name+'\n'
        for c in self.classes:
            result += c+'\n'
        return result

    def __str__(self):
        result = self.name+'\n'
        for c in self.classes:
            result += str(c)+'\n'
        return result



def main():
    parser = ParseView()
    parser.parseFile('views.sql')
    parser.createDalsView()


if __name__ == "__main__":
    main()
