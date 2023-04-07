import os

def create_txt_file(filepath):
  with open(filepath, 'w', encoding='utf-8') as f:
    f.write('')

basepath = os.path.join('.', 'Japan')
for i in range(5):
  filepath = os.path.join(basepath, 'news{}.txt'.format(i + 1))
  create_txt_file(filepath)