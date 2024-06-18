import pickle
import os
import xlsxwriter
import numpy as np
import cv2

Bordersize=100
def extract_lineage(outpath):
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")
    lineage = []
    with (open(lineage_path, "rb")) as openfile:
     while True:
        try:
            lineage.append(pickle.load(openfile))
        except EOFError:
            break    
    return lineage
###################################################
def create_lineage_per_cell(lineage_per_frame,outpath, frame_size):
  
  names=[]
  for k in range(len(lineage_per_frame)):
    item =lineage_per_frame[k]
    keys =list(item.keys())
    names+=[item[key][11] for key in keys]
  cell_names =list(set(names))# all cell names encountered in movie
  
  pedigree_per_cell ={}
  
  for name in cell_names:
 
    pedigree_per_cell[name]=[]
    for i in range(len(lineage_per_frame)):   
      item =lineage_per_frame[i]
      frame_keys =list(item.keys())
     
      for key in frame_keys:
          cell_id=item[key][11]
          if name==cell_id:
            #cell_name=item[key][11]
            frame_number=item[key][12]
            cX,cY=item[key][6][0],item[key][6][1]
            area=item[key][18]
            perimeter=item[key][19]
            circularity=item[key][20]
            bounding_box=item[key][2]
            ####
            big_patch_border=np.zeros((frame_size+2*Bordersize, frame_size+2*Bordersize), np.uint8)
            a,b,c,d=item[key][7], item[key][8],item[key][9], item[key][10]
            big_patch_border[c:d,a:b]=item[key][3]
            big_one_cell_image=big_patch_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
                       
            #####
            add=[frame_number,[cX,cY],area,perimeter,circularity, bounding_box, big_one_cell_image] 
            pedigree_per_cell[name].append(add)
                
  pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
  with open(pedigree_path, 'wb') as f:
         pickle.dump(pedigree_per_cell, f)  
  return pedigree_per_cell
###############################################
def create_lineage_for_Lorenzo(outpath, frame_size):
    print("outpath=", outpath)
    lineage_per_frame=extract_lineage(outpath)
    lineage_per_cell=create_lineage_per_cell(lineage_per_frame,outpath, frame_size)
    
    dirr=os.path.join(outpath,"CELLS_INFO_WITHOUT_DIAGRAMS_EXCEL")
    if not os.path.exists(dirr):
        os.mkdir(dirr)
    list_of_cell_names =list(lineage_per_cell.keys())
    for cell_name in list_of_cell_names:#
       path=os.path.join(dirr,cell_name)# create folders "1", "10", etc. for segmented images of each cell  
       if not os.path.exists(path):
          os.mkdir(path)
       x=lineage_per_cell[cell_name]
             
       print("path for excel=", path)
       workbook = xlsxwriter.Workbook(os.path.join(path,cell_name +".xlsx"))     
       worksheet = workbook.add_worksheet()
       worksheet.set_column('B:B',12)
       worksheet.set_column('F:F',12)
       worksheet.set_column('G:G',12)
       worksheet.set_column('C:C',5)
       worksheet.set_column('D:D',5)
       worksheet.set_column('H:H',5)
       worksheet.set_column('I:I',5)
       worksheet.set_column('J:J',5)
       worksheet.set_column('K:K',5)
       worksheet.write('A1', 'Cell name')
       worksheet.write('B1', 'Frame')
       worksheet.write('C1', 'cX')
       worksheet.write('D1', 'cY')
       worksheet.write('E1', 'Area')
       worksheet.write('F1', 'Perimeter')
       worksheet.write('G1', 'Circularity')
       worksheet.write('H1', 'x')
       worksheet.write('I1', 'y')
       worksheet.write('J1', 'w')
       worksheet.write('K1', 'h')
       
       #x=lineage_per_cell[cell_name]
       
       row = 1
       for i in range(len(x)): 
          score = [cell_name, "Frame %s" % (x[i][0]+1), x[i][1][0],x[i][1][1],x[i][2],x[i][3],x[i][4],x[i][5][0],
                   x[i][5][1],x[i][5][2],x[i][5][3]]
          ['None' if v is None else v for v in score]
          print("score=", score)
          one_cell_big_image=x[i][6]
          file_name=os.path.join(path,"cell_%s_frame_%s.tif" % (cell_name,x[i][0]+1))
          cv2.imwrite(file_name,one_cell_big_image)
          for k in range(len(score)):
            worksheet.write(row, k, score[k])
          row+=1
        
       workbook.close()
    return lineage_per_cell