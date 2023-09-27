import random

random_answers_by_index = ''

for i in range(50):
  rand_int = random.choices('1234')
  num = str(rand_int)[2]
  random_answers_by_index += f'{num},'

print(random_answers_by_index)


