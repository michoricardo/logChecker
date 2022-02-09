import csv,os
from collections import Counter
array_complete,array_error,array_process,array_report,file_array=[],[],[],[],[] #This arrays will contain the data for each line of the csv file and the files contained in the current directory
result_filename = 'resultao.csv'
def file_securrent_file(): #This method finds every file of systask to iterate and get data
    for file in os.listdir():
        if '-systask' in file and file.endswith(".csv"):
            file_array.append(file)
    print('Files found: \n',file_array)
def most(input_array,attribute,current_file_name): #This method contains the logic of the writing into the csv file
    global thewriter
    fieldnames = ['Task', 'number'] #Headers of csv
    thewriter = csv.DictWriter(csvfile,fieldnames=fieldnames)
    thewriter.writerow({'Task':attribute,'number':current_file}) #Separation on attributes for example completed, errors, reports and processes
    thewriter.writeheader()
    count = Counter(input_array)
    sort_orders = sorted(count.items(), key=lambda x: x[1], reverse=True) #Sorted by repetition from most to least repeated
    for key, value in sort_orders:
        print(key, ':', value)
        thewriter.writerow({'Task':key,'number':value})
    thewriter.writerow({'Task':'.....','number':'.....'}) #To give some space in csv file for aesthetics
def iter4file(): #This method contains the iteration for each file to call every other 
    global current_file,total_complete,total_error,total_process,total_report
    total_complete,total_error,total_process,total_report=0,0,0,0
    for current_file in file_array:
        with open(current_file, 'r') as f:
            mycsv= csv.reader(f)
            for row in mycsv:
                if 'COMPLETE' in row:
                    array_complete.append(row[1])
                if 'ERROR' in row:
                    array_error.append(row[1])
                if 'Process' in row:
                    array_process.append(row[1])
                if 'Report' in row:
                    array_report.append(row[1])
            number_complete=len(array_complete) #Saves the lenght of the current file array into a variable to add it for the totals
            number_error=len(array_error) 
            number_process=len(array_process) 
            number_report=len(array_report) 
            
            print('Completed processes: ',len(array_complete)) #After checking every line, shows the maximum of elements completed
            print('Errors: ',len(array_error))
            print('Processes: ',len(array_process))
            print('Reports: ',len(array_report))
            most(array_complete,'Completed Processes',current_file)
            most(array_error,'Errors in Processes',current_file)
            most(array_process,'Processes',current_file)
            most(array_report,'Reports',current_file)
            thewriter.writerow({'Task':'**************************','number':'*******************'}) #To separe
            thewriter.writerow({'Task':'Total completed in tenant : ','number':len(array_complete)}) #Totals from tenant
            thewriter.writerow({'Task':'Total errors in tenant : ','number':len(array_error)}) 
            thewriter.writerow({'Task':'Total processes in tenant : ','number':len(array_process)}) 
            thewriter.writerow({'Task':'Total reports in tenant : ','number':len(array_report)}) 
            thewriter.writerow({'Task':'','number':''}) #To separe
            thewriter.writerow({'Task':'','number':''}) #To separe
            total_complete= total_complete+number_complete
            total_error= total_error+number_error
            total_process= total_process+number_process
            total_report= total_report+number_report
            
            clear(array_complete) #Calls the function to clear the array for the next iteration of file
            clear(array_error)
            clear(array_process)
            clear(array_report)
         
def clear(thing): #Method to clear lists
    thing.clear()
    
# Main routine
file_securrent_file()
with open(result_filename, 'w',newline='') as csvfile:
    iter4file()
    print('\n TOTALS: \n')
    print('Total completed in all tenants:  ',total_complete)
    print('Total errors in all tenants:  ',total_error)
    print('Total processes in all tenants:  ',total_process)
    print('Total reports in all tenants:  ',total_report)
    thewriter.writerow({'Task':'Totals:  ','number':'------------------'})
    thewriter.writerow({'Task':'Total completed in all tenants ','number':total_complete})
    thewriter.writerow({'Task':'Total errors in all tenants ','number':total_error})
    thewriter.writerow({'Task':'Total processes in all tenants ','number':total_process})
    thewriter.writerow({'Task':'Total reports in all tenants ','number':total_report}) 





