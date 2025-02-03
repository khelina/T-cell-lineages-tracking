import os
software_folder = os.getcwd()
from functions import extract_lineage

#outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE r"
outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE_SHORT"

lineage_per_frame=extract_lineage(outpath)
print("len(lineage_per_frame)=",len(lineage_per_frame))

x=lineage_per_frame
x[0].keys()

check_list=[]
for i in range(len(x)):
    item=x[i]
    keys=list(item.keys())
    print("keys=", keys)
    for key in keys:        
        frame_number=item[key][12]
        centr=item[key][6]
        check_list.append((key,frame_number,centr))
    
print(check_list)

###############################
"""
def if_elif_else(x):
    if x<2:
        print("x<2")
    elif 2<=x<=10:
        print("2<=x<=10")
    else:
         print("x>2")
if_elif_else(15)
#############################
def if_else_if(x):
    if x<2:
        print("x<2")
    else:
        print("x>=2")
    if x>-1:
         print("x>-1")
if_else_if(-5)
##############################################
k=1
stop_var="No"
div_var=0
while k<10:
    print("k=", k)
    for kk in range(4):
        frame_number=k+kk
        print("frame_number=", frame_number)
        if stop_var=="Stop":
            print("stoppped small loop due to Stop")
            break
        if div_var==1:
            print("stoped small loop due to Div")
            break
    if stop_var=="Stop":
        k=k+kk+1
        print("stopped big loop due to Stop")
        break
    else:
        if div_var==1:
            k=k+kk+2
            print("continue big loop after Div")
        else:
            print("continue big loop, nithing was detected")
            k+=4
    
print("Broke out of big loop")
print("k=", k)        
"""    