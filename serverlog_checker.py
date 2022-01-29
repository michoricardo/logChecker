import csv
print("This file needs to be in the same path as the file to analyze\n")
print("\n*********************\n")

filename = input("Name of the file with extension: ")

print("\n Executing ............\n")
result_filename = "records.csv"
print(filename)
with open(result_filename, 'w',newline='') as csvfile:
    fieldnames = ['Call', 'Duration on server', 'Sql time','Difference'] #Headers of csv
    thewriter = csv.DictWriter(csvfile,fieldnames=fieldnames)
    thewriter.writeheader()
    sql_time,duration,call="-","-","-"
    
    with open(str(filename), 'r') as f:
        contents = f.readlines()
        array_call=[]
        array_dur=[]
        array_sql=[]
        array_diff=[]
        for line in contents:
            if line.startswith("<Op Utc") and ("Ice:" in line or "Erp:" in line):
                sql_time='x' #Erase value of sql time if not in this log. This assures to not overlap times if not existed
                start_dur = 'dur="'
                end_dur = '"'
                start_call = 'act="'
                end_call = '"'
                call=(line.split(start_call))[1].split(end_call)[0]
                duration=float((line.split(start_dur))[1].split(end_dur)[0])
                #print("Call name : " ,call)
                #print("Server Duration : ",duration)
                
            if "<Sql queries" in line:
                start_time = 'time="'
                end_time = '"'
                sql_time=float((line.split(start_time))[1].split(end_time)[0])
                #print("Sql Time : ",sql_time)
                
            if line.startswith("</Op>") and not "Ice:ServerLog/Initialize" in line:
                array_call.append(call)
                array_dur.append(duration)
                array_sql.append(sql_time)
                if sql_time != 'x':
                    diff=duration-sql_time
                    array_diff.append(diff)
                if sql_time == 'x':
                    array_diff.append('NONE')
            
        print('Array of calls length: ',len(array_call))
        print('Array of durations length: ',len(array_dur))
        print('Array of sql times length: ',len(array_sql))
        for i in range(len(array_call)):
            thewriter.writerow({'Call':array_call[i],'Duration on server':array_dur[i],'Sql time':array_sql[i],'Difference':array_diff[i]}) #Every row from csv is a call with its times and differences

        print("\n ***************PROCESS COMPLETED ************* \n")
        

            
            
