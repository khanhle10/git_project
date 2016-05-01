from heapq import merge

def quickSort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = quickSort(less)
        more = quickSort(more)
        return less + pivotList + more
def write_to_file(list, count):
    str_list = ','.join(str(x) for x in list)
    file = "file"
    end_file = ".txt"
    with open(file + str(count) + end_file, "w") as o_file:
        o_file.write(str_list)
        o_file.write(',')
        o_file.close()
# convert read data to int
def convert_to_int(data):
    return quickSort([int(x) for x in data.split(',') if x != '' or x == 0])

def read_file():
    buffer_size = 4*1024
    max_list = []
    max_buffer = ""
    max_buffer_size = 2*buffer_size
    count = 0
    global_count = 0
    with open("age.txt") as file:
        while True:
            data = file.read(buffer_size)
            if data == '':
                break
            max_buffer = ','.join([data,max_buffer])
            count += 1
            if count == 2:
                list_int = convert_to_int(max_buffer)
                while 0 in list_int:
                    list_int.remove(0)
                #write to file 8kb sorted increase file count
                write_to_file(list_int, global_count)
                count = 0
                global_count += 1
            # check begin two way merge sort
            if global_count > 4:
                read_set_file(global_count - 1)
# stage to start reading two files to begin merge
def read_set_file(global_count):
    file = "file"
    end_file = ".txt"
    count = 0
    print ("Global Count " + str(global_count))
    while True:
        with open(file + str(count) + end_file, "r") as r_file:
            with open(file + str(count + 1) + end_file, "r") as s_file:
                sort_read_files(r_file, s_file, count)
                count += 1
                s_file.close
            r_file.close
        if count == global_count:
            break
# merge two files
def sort_read_files(file1, file2, count):
    file = "file"
    end_file = ".txt"
    num_of_100 = 0
    with open(file + str(count - 1) + end_file, "w") as o_file:
        while True:
            n1 = file1.read(6)
            n2 = file2.read(6)
            print(n1 + " " + n2 + " count " + str(count))
            if n1 != '' and n2 != '':
                num_of_100 = write_to_file_lists(n1,n2, o_file, num_of_100)
            elif n1 == '' and n2 != '' :
                num_of_100 = check_num(n2, num_of_100, o_file)
            elif n1 != '' and n2 == '':
                num_of_100 = check_num(n1, num_of_100, o_file)
            elif n1 == '' and n2 == '':
                file1.close()
                file2.close()
                break
        write_last_count(o_file,num_of_100)
        o_file.close()

def check_num(num, count, file):
    for x in num.split(','):
        if int(x) != '':
            if int(x) != 99:
                file.write(x + ',')
            elif int(x) == 99:
                file.write(x + ',')
            else:
                count += 1
    return count

def write_to_file_lists(list1, list2, file, count):
    for (x,y) in zip(list1.split(','), list2.split(',')):
        if x != '' and y != '':
            if int(x) != 99 or int(y) != 99 or int(x) != 0 or int(y) != 0:
                if int(x) < int(y):
                    file.write(x + ',')
                elif int(x) > int(y):
                    file.write(y + ',')
                else:
                    file.write(x + ',' + y + ',')
            else:
                if int(x) == 99:
                    file.write(x + ',')
                elif int(y) == 99:
                    file.write(y + ',')
                else:
                    if int(x) == 10 or int(y) == 10:
                        count += 1
    return count

def write_last_count(file, count):
    while count > 0:
        file.write('100,')
        count -=1
read_file()
