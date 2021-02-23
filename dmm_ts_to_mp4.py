#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

path = "d:/"
m3u8_file = path + "chunklist_b600000.m3u8"
drm_key_file = path + "drm_iphone"
ts_dir = path + "download/"
ts_decrypt_dir = path + "decrypt/"
output_dir = path + "output/"
concat_file_list = path + "filelist"

count = 0

if not os.path.exists(ts_dir):
    os.mkdir(ts_dir)

if not os.path.exists(ts_decrypt_dir):
    os.mkdir(ts_decrypt_dir)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


with open(drm_key_file, "br") as f:
    drm_key = f.readline().hex().upper()
    print(drm_key)


with open(m3u8_file, "r") as f:
    count_line = f.readlines()
    count_line = count_line[-2]
    count = int(count_line.split("_")[2].split(".")[0]) + 1


for i in range(0, count):
    file_input = ts_dir + "media_b6000000_{x}.ts".format(x=i)
    file_output = ts_decrypt_dir + "media_b6000000_{x}.ts".format(x=i)
    iv = "%032x" % i
    openssl_cmd = "openssl aes-128-cbc -d -in {file_input} -out {file_output} -K {k} -iv {iv} -nosalt".\
        format(file_input=file_input, file_output=file_output, iv=iv, k=drm_key)
    #print(openssl_cmd)
    os.system(openssl_cmd)
    # os 调用cmd

with open(concat_file_list, "w+") as f:
    for i in range(0, count):
        file = ts_decrypt_dir + "media_b6000000_{x}.ts".format(x=i)
        line = "file '{file}'\n".format(file=file)
        f.write(line)


output_file = output_dir + "output.mp4"
ffmpeg_cmd = "ffmpeg -f concat -safe 0 -i {concat_file_list} -c copy {output_file}".\
    format(concat_file_list=concat_file_list, output_file=output_file)
os.system(ffmpeg_cmd)

