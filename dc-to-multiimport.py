import pandas as pd
import numpy as np
import re

def AddDCFieldQualifier(dc, listOfFields):
    # adds a string of ~ and a qualifier for columnts that need a qualifier i.e. Personal_Name~Roles
   
    listOfFields = MatchString(dc, listOfFields)

    for field in listOfFields:
        pattern = re.search('(?<=\.)[a-z]*', field)

    
    
        dc[field] = dc[field].astype(str) + "~" + pattern.group(0)

    #replaces blank fields with NaN instead of the string: nan~qualifer    
    dc = dc.replace(r'nan.+', np.nan, regex=True)
    return dc
    
def AddNewQualifier(dc, field, qualifier):
    #adds a subfield that have a different name than the dc field, ie Public_Notes~Types and ~statement of responsibility
   
    dc[field] = dc[field].astype(str) + qualifier
    
    #replaces blank fields with NaN instead of the string: nan~qualifer
    dc = dc.replace(r'nan.+', np.nan, regex=True)

        
   
    return dc
    
    

        
def MatchString(dc, columnnamematch):
    #Matches columns from the orginal spreadsheet with columns that share the same name and a number, i.e. Contributer 1
    listofcolumns = []
    allcolumns = dc.columns
    for columnname in columnnamematch:
    
        pattern = re.compile('^' + columnname + '.*')
    
        for name in allcolumns:
            if (pattern.search(name)):
                listofcolumns.append(name)
    return listofcolumns        



def MultipleField (dc, listOfFields, valueString):
    
    #concoconates fields with multiple columns
    
    listOfFields = MatchString(dc, listOfFields)
    
    
    if listOfFields == []:
        
        pass
     
    else: 
        valueString = dc[listOfFields].apply(lambda x: x.str.cat(sep= ' | '), axis=1)

        
    
    return valueString
        
    
def main(dc, newcsv):
    df = pd.read_csv(dc)
    df = AddDCFieldQualifier(df, ['dc.creator', 'dc.contributor'])
    df = AddNewQualifier(df, 'dc.rights', '~statement of responsibility')
    df = AddNewQualifier(df, 'dc.relation', '~host')
    df = AddNewQualifier(df, 'dcterms.source', '~original')
   
    
    df2 = pd.DataFrame({'STATUS' : 'This is the ' + df['dc.title'] + ' parent',
                        'OBJ' : MultipleField(df,['filename'], ''),
                        'Title' : MultipleField(df,['dc.title'], ''),
                       'Alternative_titles' : MultipleField(df, ['dc.subtitle'], ''), 
                       'Personal_Names~Roles' : MultipleField(df,['dc.creator', 'dc.contributor'], ''),
                       'Corporate_Names~Roles' : np.nan,
                       'Hidden_Creator' : np.nan,
                       'Abstract' : MultipleField(df, ['dcterms.abstract', 'dc.description'], ''),
                       'Pull_Quotes' : np.nan,
                       'Index_Date' : np.nan,
                       'Other_Date~Display_Label' : np.nan,
                       'Date_Issued' : df['dc.date'],
                       'Publisher' : MultipleField(df, ['dc.publisher'], ''),
                       'Place_Of_Publication' : np.nan,
                       'Public_Notes~Types' : MultipleField(df, ['dc.rights'], ''),
                        'Private_Notes~Types' : np.nan,
                        'Keywords' : np.nan, 
                        'LCSH_Subjects' : MultipleField(df, ['dc.subject'], ''),
                       'Subjects_Temporal' : np.nan,
                       'Subjects_Geographic' : MultipleField(df, ['dc.coverage'], ''),
                       'Subjects_Names~Types' : np.nan,
                       'Coordinate' : np.nan,
                       'Type_of_Resource' : MultipleField(df, ['dc.type'], ''),
                       'Genre' : np.nan,
                       'Extent' : MultipleField(df, ['image specifications'], ''),
                       'Form' : np.nan,
                       'MIME_Type' : MultipleField(df, ['dc.format'], ''),
                       'Digital_Origin' : np.nan,
                       'Language_Names~Codes' : MultipleField(df, ['dc.language'], ''),
                       'Local_Identifier' : df['dc.identifier'],
                       'Physical_Location' : MultipleField(df, ['physical location'], ''),
                       'Shelf_Locator' : np.nan,
                       'Classifications~authorities' : np.nan,
                       'Related_Items~types' : MultipleField(df, ['dc.relation', 'dcterms.source'], ''),
                      'Access_Condition' : MultipleField(df, ['dcterms.accessRights'], '')})
    
    columnsTitles = ['PID','STATUS','Import_Index', 'CMODEL', 'SEQUENCE', 'OBJ','Title','Alternative_titles','Personal_Names~Roles', 'Corporate_Names~Roles', 'Hidden_Creator', 'Abstract', 'Pull_Quotes', 'Index_Date', 'Other_Date~Display_Label', 'Date_Issued', 'Publisher', 'Place_Of_Publication', 'Public_Notes~Types', 'Private_Notes~Types', 'Keywords', 'LCSH_Subjects', 'Subjects_Temporal', 'Subjects_Geographic', 'Subjects_Names~Types', 'Coordinate',  'Type_of_Resource' , 'Genre', 'Extent', 'Form', 'MIME_Type', 'Digital_Origin', 'Language_Names~Codes', 'Local_Identifier', 'Physical_Location', 'Shelf_Locator', 'Classifications~authorities', 'Related_Items~types', 'Access_Condition']
    
    df2 = df2.reindex(columns=columnsTitles)
    
    df2.to_csv(newcsv)
    
    return df2

main('metadata.csv', 'foo.csv')





