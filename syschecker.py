import csv,os,warnings
from collections import Counter
array_complete,array_error,array_process,array_report,file_array,file2_array,errorcheck_array,reasons_array=[],[],[],[],[],[],[],[] #This arrays will contain the data for each line of the csv file and the files contained in the current directory
result_filename = 'results_systask.csv'
def file_securrent_file(): #This method finds every file of systask and systaskLog to iterate and get data
    for file in os.listdir():
        if '-systask' in file and file.endswith(".csv"):
            file_array.append(file)
        if '-SysTaskLog' in file and file.endswith(".csv"):
            file2_array.append(file)        
    print('Files found for data of tasks: \n',file_array)
    print('Files found for data of errors: \n',file2_array)
    
def most(input_array,attribute,current_file_name): #This method contains the logic of the writing into the csv file
    thewriter.writerow({'Task':attribute,'number':current_file}) #Separation on attributes for example completed, errors, reports and processes
    thewriter.writeheader()
    count = Counter(input_array)
    sort_orders = sorted(count.items(), key=lambda x: x[1], reverse=True) #Sorted by repetition from most to least repeated
    for key, value in sort_orders:
        thewriter.writerow({'Task':key,'number':value})
    separator(1)
    
def iter4file(): #This method contains the iteration for each file to call every other 
    global current_file,total_complete,total_error,total_process,total_report
    total_complete,total_error,total_process,total_report=0,0,0,0
    for current_file in file_array:
        with open(current_file, 'r') as f:
            mycsv= csv.reader(f)
            for row in mycsv:
                if 'COMPLETE' in row:
                    array_complete.append(row[1])
                if 'ERROR' in row or 'Error' in row:
                    array_error.append(row[1])
                    errorcheck_array.append(row[0]) #This saves the systasknum into an array to check it later
                if 'Process' in row:
                    array_process.append(row[1])
                if 'Report' in row:
                    array_report.append(row[1])
            number_complete=len(array_complete) #Saves the lenght of the current file array into a variable to add it for the totals
            number_error=len(array_error) 
            number_process=len(array_process) 
            number_report=len(array_report)
            error_checker(current_file,errorcheck_array)
            print('Completed processes: ',len(array_complete)) #After checking every line, shows the maximum of elements completed
            print('Errors: ',len(array_error))
            print('Processes: ',len(array_process))
            print('Reports: ',len(array_report))
            most(array_complete,'Completed Processes',current_file) #Calls the function to sort and write the data of processes, reports, errors, etc.
            most(array_error,'Errors in Processes',current_file)
            most(array_process,'Processes',current_file)
            most(array_report,'Reports',current_file)
            thewriter.writerow({'Task':'Total completed in tenant : ','number':len(array_complete)}) #Totals from each tenant
            thewriter.writerow({'Task':'Total errors in tenant : ','number':len(array_error)}) 
            thewriter.writerow({'Task':'Total processes in tenant : ','number':len(array_process)}) 
            thewriter.writerow({'Task':'Total reports in tenant : ','number':len(array_report)})
            separator(2)
            total_complete= total_complete+number_complete #Add numbers from current tenant to totals
            total_error= total_error+number_error
            total_process= total_process+number_process
            total_report= total_report+number_report            
            clear(array_complete) #Calls the function to clear the array for the next iteration of file
            clear(array_error)
            clear(array_process)
            clear(array_report)
            clear(errorcheck_array) #Clears the systasknums for the next iteration of file
            clear(reasons_array) #Clear all the messages from systaskLog reasons of failure on ERP
            
         
def clear(thing): #Method to clear lists
    thing.clear()
def error_checker(current_file,errorcheck_array):
    #Takes current file to work with the SysTaskLog.csv file according to the systask.csv file. That's why naming is important
    print("Current file: ", current_file)
    tenant_prefix = (current_file.partition('-')[0])
    print(tenant_prefix)
    constructed_file=tenant_prefix+'-SysTaskLog.csv'
    print('We will check this file: ', constructed_file)
    with open(constructed_file, 'r') as cons:
        mycsv2= csv.reader(cons)
        for row2 in mycsv2: #For each row in the csv file will be checking each of the elements in the array
            for systasknum in errorcheck_array:
                if systasknum in row2:
                    trunc = (row2[4])[:40] #This index contains the MsgText attribute of the csv file according to the systasknum (TRUNCATES TO 40 CHARS BECAUSE TOO LONG ERRORS)
                    if not trunc.startswith('Program'): #Skip Program warnings that are also saved in systaskLog files with systasknum index, We don't need them
                        reasons_array.append(trunc)
        count2 = Counter(reasons_array)
        sort_reasons = sorted(count2.items(), key=lambda x: x[1], reverse=True) #Sorted by repetition from most to least repeated
        thewriter.writerow({'Task':'Reasons of failure in ERP','number':current_file})
        for key2, value2 in sort_reasons:
            thewriter.writerow({'Task':key2,'number':value2})
        thewriter.writerow({'Task':'.....','number':'.....'}) #To give some space in csv file for aesthetics

def separator(kind): #Handles the kind of separator in the csv file
    if kind == 1:
        thewriter.writerow({'Task':'---------------------------','number':'---------------------------'}) #To separe from each group of data in the same tenant
    if kind == 2:
        thewriter.writerow({'Task':'','number':''}) #To separe from each tenant findings
        thewriter.writerow({'Task':'***************************','number':'***************************'}) 
        thewriter.writerow({'Task':'---------------------------','number':'---------------------------'}) 
        thewriter.writerow({'Task':'***************************','number':'***************************'}) 
        thewriter.writerow({'Task':'','number':''})
    if kind == 3:
        thewriter.writerow({'Task':'','number':''}) #To separe from each tenant findings
        thewriter.writerow({'Task':'@@@@@@@@@@@@@@@@@@@@@@@@@@@','number':'@@@@@@@@@@@@@@@@@@@@@@@@@@@'}) 
        thewriter.writerow({'Task':'---------------------------','number':'---------------------------'}) 
        thewriter.writerow({'Task':'@@@@@@@@@@@@@@@@@@@@@@@@@@@','number':'@@@@@@@@@@@@@@@@@@@@@@@@@@@'})
        thewriter.writerow({'Task':'','number':''})
   
        
# Main routine
warnings.warn("\nNaming is important, please name your files with the following convention: t0-systask.csv and t0-SystaskLog.csv\n")
file_securrent_file()
with open(result_filename, 'w',newline='') as csvfile:
    fieldnames = ['Task', 'number'] #Headers of csv
    thewriter = csv.DictWriter(csvfile,fieldnames=fieldnames) #Creates a csv writer that will be used 
    iter4file()
    print('\nTOTALS: \n')
    print('Total completed in all tenants:  ',total_complete)
    print('Total errors in all tenants:  ',total_error)
    print('Total processes in all tenants:  ',total_process)
    print('Total reports in all tenants:  ',total_report)
    separator(3)
    thewriter.writerow({'Task':'Total completed in all tenants ','number':total_complete})
    thewriter.writerow({'Task':'Total errors in all tenants ','number':total_error})
    thewriter.writerow({'Task':'Total processes in all tenants ','number':total_process})
    thewriter.writerow({'Task':'Total reports in all tenants ','number':total_report}) 





