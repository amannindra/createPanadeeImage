
import random

random_list = [random.randint(1, 20) for _ in range(100)]


test_list = random_list[45:50]



new_list = []

print(random_list)
print(test_list)

start = -1

for i in range(len(random_list) - len(test_list) + 1):
  if random_list[i:i+len(test_list)] == test_list:
    start = i
    break

if start != -1:
    end = start + len(test_list) - 1 
    print(f"Match found from index {start} to {end}")
else:
    print("Test list not found in random list.")
    
    

random_list.insert(start, "START")
random_list.insert(end + 2, "END")

print(random_list)
    


    
    
    




        
        



