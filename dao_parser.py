import os
import datetime

now = datetime.datetime.now()
f = open('create.sql', 'r')


##-----------------------------------------------
##  PACKAGES LIST
##-----------------------------------------------
basePackageName = 'com.kayentis.epro'

sqliteManager = '.sqlite.manager'
contentprovider = '.sqlite.contentprovider'
dao = '.sqlite.dao'
daoInterface = '.sqlite.dao.extended.interfaces'
daoExtended = '.sqlite.dao.extended'
dal = '.sqlite.dal'
dalWrapper = '.sqlite.dal.wrapper'
cursor = '.sqlite.cursor'

##-----------------------------------------------
baseFileDIR = './com/kayentis/epro/sqlite'

ProviderFilesDIR = baseFileDIR+'/contentprovider'
DalFilesDir = baseFileDIR+'/dal'
DalWrapperFileDir = baseFileDIR+'/dal/wrapper'
CursorFileDir = baseFileDIR+'/cursor'
DaoFileDir = baseFileDIR+'/dao'
DaoExtendFileDir = baseFileDIR+'/dao/extended'
DaoInterfacesFileDir = DaoExtendFileDir+'/interfaces'

tableList = []
columnList = []




##---------------------------------------------------------------------------------------------
##Parse the lines of the sql file - adds the table names
##-------------------------------------------------
def parseCreateDB(line):
        index = str(line).find('CREATE TABLE')
        if index != -1:
                print('   ...new table found')
                index_ = str(line).index('"')
                newtable = str(line).split('"',2)
                tableList.append(newtable[1])
                print(newtable[1])
        else:
                parseCreateDBCOlumns(line)
                
##Parse the lines for columns detect with type
##-------------------------------------------------               
def parseCreateDBCOlumns(line):
        index = str(line).find('  "')
        if index != -1:
                newcolumn = str(line).split('"',2)
                foundType = False
                columnType = 'Object'
                nullable = not("NOT NULL" in line);
                autoIncrement = "AUTOINCREMENT" in line;
                types = ['INTEGER', 'VARCHAR', 'BIT', 'FLOAT', 'DATETIME', 'BLOB', 'TEXT']
                i = 0
                while ((not foundType) and i<(len(types))):
                        type_ = str(line).find(types[i]),
                        print('      ...#Line :'+str(line)),
                        if type_[0] != -1:
                             foundType = True
                             print('      ...#type detected:'+str(type_))
                        if not foundType:
                                i += 1
                print('      ...type detected:'+types[i])
                if foundType:
                        if i == 0:
                                columnType = 'int'
                        elif i==1:
                                columnType = 'String'
                        elif i==2:
                                columnType = 'boolean'
                        elif i==3:
                                columnType = 'float'
                        elif i==4:
                                columnType = 'Date'
                        elif i==5:
                                columnType = 'byte[]'
                        elif i==6:
                                columnType = 'String'
                print('      ...new Column found :: '+newcolumn[1]+' type :'+columnType+' Nullable :'+str(nullable))
                columnList.append((tableList[len(tableList)-1], newcolumn[1], columnType, nullable, autoIncrement))


       

##---------------------------------------------------------------------------------------------
##create the CONTENTPRovider FILES from table and colums
##-------------------------------------------
def createProvider(tablename):
        print('      ...creating Content Provider :'+tablename+'ContentProvider.java')
        pattern = 'package '+basePackageName+contentprovider+';\n '
        pattern += '\n \n'
        pattern += 'import '+basePackageName+'.sqlite.DbManager;\n'
        pattern += '\n'
        pattern += 'import android.content.ContentProvider;\n'
        pattern += 'import android.content.ContentValues;\n'
        pattern += 'import android.database.Cursor;\n'
        pattern += 'import '+basePackageName+dal+'.'+tablename+';\n'
        pattern += 'import android.content.UriMatcher;\n'
        pattern += 'import android.database.sqlite.SQLiteDatabase;\n'
        pattern += 'import android.database.sqlite.SQLiteQueryBuilder;\n'
        pattern += 'import android.net.Uri;\n'
        pattern += ''
        pattern += ''
        pattern += '\n'
        pattern += 'public class '+tablename+'ContentProvider extends ContentProvider {\n'
        pattern += '    private DbManager dbManager;\n'
        pattern += '    private static final String BASE_PATH = "'+tablename+'";\n'
        pattern += '\n'
        pattern += '    public static final String AUTHORITY = "com.kayentis.epro.sqlite.contentprovider.'+tablename+'ContentProvider";\n'
        pattern += '    public static final Uri CONTENT_URI = Uri.parse("content://" +AUTHORITY+ "/" + BASE_PATH);\n'
        pattern += '    public static final String TYPE = "'+tablename+'";\n'
        pattern += '\n'
        pattern += '    private static final int DEFAULT_CODE = 1;\n'
        pattern += '    private static final UriMatcher sURIMatcher = new UriMatcher(UriMatcher.NO_MATCH);\n'
        pattern += '        static {\n'
        pattern += '            sURIMatcher.addURI(AUTHORITY, BASE_PATH, DEFAULT_CODE);\n'
        pattern += '    }\n'
        pattern += '\n'
        pattern += '    @Override\n'
        pattern += '    public int delete(Uri uri, String selection, String[] selectionArgs) {\n'
        pattern += '        SQLiteDatabase database = dbManager.getWritableDatabase();\n'
        pattern += '        int nb = database.delete('+tablename+'.TABLE_NAME, selection, null);\n'
        pattern += '        if(nb>0) {\n'
        pattern += '            getContext().getContentResolver().notifyChange(uri,null);\n'
        pattern += '        }\n'
        pattern += '        return nb;\n'
        pattern += '    }\n \n'
        pattern += '    @Override\n'
        pattern += '    public String getType(Uri uri) {\n'
        pattern += '        return '+tablename+'ContentProvider.TYPE;\n'
        pattern += '    }\n \n'
        pattern += '    @Override\n'
        pattern += '    public Uri insert(Uri uri, ContentValues values) {\n'
        pattern += '        SQLiteDatabase database = dbManager.getWritableDatabase();\n'
        pattern += '        long id = database.insert('+tablename+'.TABLE_NAME, null, values);\n'
        pattern += '        if(id>0) {\n'
        pattern += '            getContext().getContentResolver().notifyChange(uri,null);\n'
        pattern += '            return Uri.parse(String.valueOf(id));\n'
        pattern += '        }\n'
        pattern += '        return null;\n'
        pattern += '    }\n \n'
        pattern += '    @Override\n'
        pattern += '    public boolean onCreate() {\n'
        pattern += '        dbManager =  DbManager.getInstance(getContext());\n'
        pattern += '        return false;\n'
        pattern += '    }\n \n'
        pattern += '    @Override \n'
        pattern += '    public Cursor query(Uri uri, String[] projection, String selection,String[] selectionArgs, String sortOrder) { \n'
        pattern += '        SQLiteDatabase database =  dbManager.getReadableDatabase();\n'
        pattern += '        SQLiteQueryBuilder queryBuilder = new SQLiteQueryBuilder();\n'
        pattern += '        String groupBy = "";\n'
        pattern += '\n'
        pattern += '        queryBuilder.setTables('+tablename+'.TABLE_NAME);\n'
        pattern += '        int uriType = sURIMatcher.match(uri);\n'
        pattern += '        Cursor cursor = queryBuilder.query(database,null,selection,null,groupBy,null,null);\n'
        pattern += '        cursor.setNotificationUri(getContext().getContentResolver(), uri);\n'
        pattern += '        return cursor;\n'
        pattern += '    }\n \n'
        pattern += ''
        pattern += '    @Override\n'
        pattern += '    public int update(Uri uri, ContentValues values, String selection,String[] selectionArgs) {\n'
        pattern += '        SQLiteDatabase database = dbManager.getWritableDatabase();\n'
        pattern += '        int nbColumn = database.update('+tablename+'.TABLE_NAME, values, selection, selectionArgs);\n'
        pattern += '        if(nbColumn > 0) {\n'
        pattern += '            getContext().getContentResolver().notifyChange(uri, null);\n'
        pattern += '        }\n'
        pattern += '        return nbColumn;\n'
        pattern += '    }\n'
        pattern += ''
        pattern += '}'
        writeToFile(pattern,ProviderFilesDIR+"/"+""+tablename+"ContentProvider.java")
        
##---------------------------------------------------------------------------------------------
##create the models classes 
##-------------------------------------------
def createModel(tablename):
        print('      ...creating DAL :'+tablename+".java")
        pattern = 'package '+basePackageName+dal+';'
        pattern += '\n \n'
        pattern += "import java.io.Serializable;\n"
        pattern += "import java.util.Date;\n"
        pattern += "/*\n"
        pattern += "* AUTO GENERATED FILE \n"
        pattern += "* creation date : "+now.strftime("%Y-%m-%d %H:%M")+" \n"
        pattern += "*/\n"
        pattern += "public class "+tablename+" implements Serializable { \n"
        pattern += "\n"
        pattern += "    public static String TABLE_NAME = \""+tablename+"\"; \n"
        for column in columnList:
                if column[0]==tablename:
                        colname=column[1].upper()
                        colname_=column[1]
                        pattern_column = "    public final static String COLUMN_"+colname+"=\""+colname_+"\"; \n"
                        content=pattern_column
                        pattern+= content
        pattern+= "\n"
        for column in columnList:
                if column[0]==tablename:
                        pattern += "    private "+column[2]+" "+column[1]+";\n"
        pattern += "\n"
        for column in columnList:
                if column[0]==tablename:
                        pattern += "    public "+column[2]+" get"+column[1]+"() { \n"
                        pattern += "        return "+column[1]+";\n"
                        pattern += "    }\n"
                        pattern += "\n"
                        pattern += "    public void set"+column[1]+"("+column[2]+" obj) {\n"              
                        pattern += "        this."+column[1]+" = obj;\n"
                        pattern += "    }\n"
        pattern += "}\n"
        writeToFile(pattern,DalFilesDir+"/"+tablename+".java")


##---------------------------------------------------------------------------------------------
##create the DAL WRAPPER  classes 
##-------------------------------------------
def createDalWrapper(tablename):
        print('      ...creating DALWRAPPER FOR TABLE :'+tablename)
        pattern = ''
        pattern += 'package '+basePackageName+dalWrapper+';\n\n'
        pattern += 'import android.content.ContentValues;\n'
        pattern += 'import java.io.Serializable;\n'
        pattern += 'import '+basePackageName+'.sqlite.utils.DateGetter;\n'
        pattern += 'import '+basePackageName+dal+'.'+tablename+';\n'
        pattern += 'import '+basePackageName+cursor+'.'+tablename+'Cursor;\n'
        pattern += 'import java.util.Date;\n'
        pattern += '\n'
        pattern += ''
        pattern += ''
        pattern += ''
        pattern += "/*\n"
        pattern += "* AUTO GENERATED FILE \n"
        pattern += "* creation date : "+now.strftime("%Y-%m-%d %H:%M")+" \n"
        pattern += "*/\n"
        pattern += 'public class '+tablename+'DalWrapper {\n'
        pattern += '\n'
        pattern += '    public static '+tablename+' getObjectFromDB('+tablename+'Cursor cursor, int start) { \n'
        pattern += "        "+tablename+" object_ = new "+tablename+"();\n"
        i_ =0 
        for column in columnList:
                if column[0]==tablename:
                        type = ""
                        if column[2]== "boolean":
                                type = "Int"
                                pattern += "        object_.set"+column[1]+""
                                pattern += "(cursor.get"+type+"("+str(i_)+"+start) == 0 ? false : true );\n"
                        elif column[2]== "Date":
                                type = "Int"
                                pattern += "        Date date = DateGetter.getInstance().getDateFromString(cursor.getString("+str(i_)+"+start));\n"
                                pattern += "        object_.set"+column[1]+""
                                pattern += "(date);\n"
                        elif column[2]== "byte[]":
                                type = "byte[]"
                                pattern += "        object_.set"+column[1]+""
                                pattern += "(cursor.getBlob("+str(i_)+"+start));\n"
                        else:             
                                type = str(column[2][0]).upper()+column[2][1:]
                                pattern += "        object_.set"+column[1]+""
                                pattern += "(cursor.get"+type+"("+str(i_)+"+start));\n"
                        i_+=1
        pattern += "        return object_;\n"
        pattern += '    }\n\n'
        pattern += "    public static int getNbColumns() { \n"
        pattern += "        return "+str(i_)+";\n"
        pattern += "    }\n\n"
        pattern += ''
        pattern += "    public static ContentValues getContentValueFromObject(Serializable object) { \n"
        pattern += "        "+tablename+" object_ = ("+tablename+") object;\n"
        pattern += "        ContentValues values = new ContentValues();\n"
        for column in columnList:
                if column[0] == tablename:
                        if column[2] == 'Date':
                                pattern += "        String dateString = DateGetter.getInstance().getStringFromDate("
                                pattern += "object_.get"+column[1]+"()"
                                pattern += ");\n"
                                pattern += "        values.put("+tablename+".COLUMN_"+column[1].upper()+",dateString);\n"
                        elif column[2] != 'Date' and not(column[4]):
                                pattern += "        values.put("+tablename+".COLUMN_"+column[1].upper()+","
                                pattern += "object_.get"+column[1]+"()"
                                pattern += ");\n"
        pattern += "        return values;\n"
        pattern += "    }\n"
        pattern += "\n"
        pattern += '}'
        pattern += ''
        pattern += ''
        pattern += ''
        pattern += ''
        pattern += ''
        writeToFile(pattern,DalWrapperFileDir+"/"+tablename+"DalWrapper.java")
        


##---------------------------------------------------------------------------------------------
##create DAO classes 
##-------------------------------------------
def createDAO(tablename):
        print('      ...creating DAO FOR TABLE :'+tablename)
        pattern = 'package '+basePackageName+daoExtended+';\n\n'
        pattern += 'import android.content.Context;\n'
        pattern += 'import '+basePackageName+dalWrapper+'.'+tablename+'DalWrapper;\n\n'
        pattern += 'import android.database.Cursor;\n'
        pattern += 'import android.net.Uri;\n'
        pattern += 'import android.util.Log;\n'
        pattern += 'import '+basePackageName+contentprovider+'.'+tablename+'ContentProvider;\n'
        pattern += 'import '+basePackageName+dao+'.BaseDAO;\n'
        pattern += 'import '+basePackageName+dal+'.'+tablename+';\n'
        pattern += 'import '+basePackageName+daoInterface+'.I'+tablename+';\n'
        pattern += '\n'
        pattern += 'public class '+tablename+'DAO extends BaseDAO implements I'+tablename+' {\n\n'
        pattern += '    private final static String TAG = '+tablename+'DAO.class.getName();\n\n'
        pattern += '    public '+tablename+'DAO(Context c) {\n'
        pattern += '        super(c, '+tablename+'ContentProvider.CONTENT_URI);\n'
        pattern += '    }\n\n'
        pattern += ''
        pattern += '    @Override\n'
        pattern += '    public int save('+tablename+' element) {\n'
        pattern += '       int result = add('+tablename+'DalWrapper.getContentValueFromObject(element));\n'
        pattern += '       return result;\n'
        pattern += '    }\n'
        pattern += ''
        pattern += '}\n'
        
        writeToFile(pattern,DaoExtendFileDir+"/"+tablename+"DAO.java")


##---------------------------------------------------------------------------------------------
##create EXTENDED DAO interfaces 
##-------------------------------------------
def createExtendedInterfaceDAO(tablename):
        print('      ...creating DAO FOR TABLE :'+tablename)
        pattern = 'package '+basePackageName+daoInterface+';\n\n'
        pattern += 'import '+basePackageName+dal+'.'+tablename+';\n'
        pattern += '\n'
        pattern += 'public interface I'+tablename+'{\n'
        pattern += ''
        pattern += '  public int save('+tablename+' element);'
        pattern += ''
        pattern += ''
        pattern += '}\n'
        
        writeToFile(pattern,DaoInterfacesFileDir+"/I"+tablename+".java")        

##---------------------------------------------------------------------------------------------
##create the CURSOR WRAPPER  classes 
##-------------------------------------------
def createCursorImpl(tablename):
        print('      ...creating Cursor FOR TABLE :'+tablename)
        pattern = ''
        pattern += 'package '+basePackageName+cursor+';\n'
        pattern += '\n'
        pattern += 'import android.content.Context;\n'
        pattern += 'import android.database.Cursor;\n'
        pattern += 'import android.net.Uri;\nimport android.database.CursorWrapper;\n'
        pattern += '\n'
        pattern += 'public class '+tablename+'Cursor extends CursorWrapper {\n'
        pattern += '\n'
        pattern += '\n'
        pattern += '    public '+tablename+'Cursor(Cursor c) {\n'
        pattern += '        super(c);\n'
        pattern += '    }\n'
        pattern += '\n'
        pattern += '}'
        pattern += ''
        pattern += ''
        writeToFile(pattern,CursorFileDir+"/"+tablename+"Cursor.java")


##---------------------------------------------------------------------------------------------
##create provider in manifest  
##-------------------------------------------
def createManifest():
        pattern = ''
        for tablename in tableList:
                print('       ...creating manifest entry for Content Provider '+tablename)
                pattern += '<provider \n'
                pattern += '    android:name="'+basePackageName+contentprovider+'.'+tablename+'ContentProvider" \n'
                pattern += '    android:authorities="'+basePackageName+contentprovider+'.'+tablename+'ContentProvider" \n'
                pattern += '    android:enabled="true"\n'
                pattern += '    android:exported="false" >\n'
                pattern += '</provider>\n'
        writeToFile(pattern,"./manifestEntries.xml")

        
##---------------------------------------------------------------------------------------------
##Create a new
## @param content - string for the content
## @param filename - string for the name of the file
##-------------------------------------------------
def writeToFile(content,filename):
        out = open(filename,'w')
        out.write(content)
        print("..."+filename+" created")

##---------------------------------------------------------------------------------------------
##create the files for each tables -> DAO and interfaces
##------------------------------------------------- 
def createDAOFILE():
        for table in tableList:
                createProvider(table)
                createModel(table)
                createDalWrapper(table)
                createCursorImpl(table)
                createExtendedInterfaceDAO(table)
                createDAO(table)
        createManifest()

##---------------------------------------------------------------------------------------------
        

## EXECUTION PART
##*****************************
for line in f:
        parseCreateDB(line)


print('------------------------------')
print('...CREATING DAO FILES ')
print('------------------------------')

print('   ...creating directories:')
if not os.path.exists(baseFileDIR):
        os.makedirs(baseFileDIR)
if not os.path.exists(ProviderFilesDIR):
        os.makedirs(ProviderFilesDIR)
if not os.path.exists(DalFilesDir):
        os.makedirs(DalFilesDir)
if not os.path.exists(DalWrapperFileDir):
        os.makedirs(DalWrapperFileDir)
if not os.path.exists(CursorFileDir):
        os.makedirs(CursorFileDir)
if not os.path.exists(DaoExtendFileDir):
        os.makedirs(DaoExtendFileDir)
if not os.path.exists(DaoFileDir):
        os.makedirs(DaoFileDir)
if not os.path.exists(DaoInterfacesFileDir):
        os.makedirs(DaoInterfacesFileDir)

        
createDAOFILE()
        

print('#File creation ended successfully : ')
print(str(len(tableList))+' table(s) have been parsed.')
        
os.system("pause")
