import os
import threading
import time



path = "d:/work/"
m3u8_file = path + "chunklist_b600000.m3u8"
drm_key_file = path + "drm_iphone"
ts_raw_dir = path + "raw/"
ts_decryp_dir = path + "de/"
ts_merge_dir = path + "merge/"


count = 0
drm_key = ''
thread_count = 8 
mount = 53 
res = []
for i in range(1, mount+1):
    res.append(i)
step = mount // 8 

def fun(res):
    print(res)
    for i in res:
        time.sleep(1)
        print(i)

for i in range(1,8+1):
    if(i != 8):
        #print((i-1)*step, i*step-1)
        _a = res[(i-1)*step : i*step-1] 
        #print(type(_a))
        #print(_a)
        threading.Thread(target=fun, args=(_a,)).start()
    else:
        #print((i-1)*step,mount-1)
        _b = res[(i-1)*step : mount-1]
        threading.Thread(target=fun, args=(_b,)).start()
    
#time.sleep(10000)


mount = 300
thread = 8


exit()

## 读取key
with open(drm_key_file,"br") as f:
    drm_key = f.readline().hex().upper()
    print(drm_key)

## 读取总片段数目
with open(m3u8_file,"r") as f:
    count_line = f.readlines()
    count_line = count_line[-2]
    count = 1900

print(count)


## 解密
with open(path + "/de.bat","w+") as f:
    for i in range(0,count):
        line = "openssl aes-128-cbc -d -in ./media_b6000000_{x}.ts -out {c}/{y}.ts -K {k} -iv {z} -nosalt \n".format(x=i, y=i,z="%032x"%i,k=drm_key,c=ts_decryp_dir)
        f.write(line)

    f.write("pause()")
    
## 合并
with open(path + "./filelist","w+") as f:
    for i in range(0,count):
        line = "file '{c}{x}.ts'\n".format(x=i,c=ts_decryp_dir)
        f.write(line)

#  -vcodec copy -acodec copy
'''
143
141
140 -
139
138 -
132
118 
'''



