import re
# clean data entries with extra \n and move broken lines into one line
def func(filename1, filename2):
    inputfile = open(filename1, 'r')
    content = inputfile.read()
    result = re.sub('\s*\\\s*\n','', content)
    outputfile = open(filename2, 'w')
    outputfile.write(result)
    outputfile.close()
    inputfile.close()

# do cleaning for all 25 files
for i in range(1, 25):
    filename1 = "greenwich_tags_full_image_nwu_202092_" + str(i) + "_202092.part_00000"
    filename2 = "tags_" + str(i)
    func(filename1, filename2)
