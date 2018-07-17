# Варианты конкатенации файлов с конфигами и карты vlanmap, оставил наиболее оптимальный без комментов,
# хотя, может, лучше этого не делать, а положить эти вланы в глобальные переменные.
#
#
# добавление в конец конфига списка вланов - к списку вланов можно обращаться с конца

filenames = ['file1.txt', 'file2.txt']
for fname in filenames:
    with open(fname, 'a') as outfile:
        with open('vlans.txt') as infile:
            outfile.write(infile.read())

# создание нового файла - создание лишних объектов, нагрузка на память
#
# filenames = ['file1.txt', 'file2.txt']
# count = 1
# for fname in filenames:
#     with open('file_final'+str(count)+'.txt', 'w') as outfile:
#         with open('vlans.txt') as infile:
#             for line in infile:
#                 outfile.write(line)
#         with open(fname) as infile:
#             for line in infile:
#                 outfile.write(line)
#     count += 1


# еще вариант с созданием нового файла, но требует меньше памяти
#
# import shutil
# filenames = ['file1.txt', 'file2.txt']
# count = 1
# for fname in filenames:
#     with open('file_final'+str(count)+'.txt', 'w') as outfile:
#         with open('vlans.txt') as vlans, open(fname) as config:
#             shutil.copyfileobj(vlans,outfile)
#             shutil.copyfileobj(config,outfile)
#     count += 1


# изменение файла конфига с добавлением в начало вланов,
# занимая память содержимым вланов и самого конфига
#
# filenames = ['file1.txt', 'file2.txt']
# with open('vlans.txt') as infile:
#     vlans = infile.read()
#     for fname in filenames:
#         with open(fname) as outfile_read:
#             config = outfile_read.read()
#         with open(fname, 'w') as outfile:
#             print(vlans,config,sep='\n',file=outfile)
