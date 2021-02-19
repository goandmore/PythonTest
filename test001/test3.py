from hashlib import sha256
x = 1256
y = 0  # y未知
while sha256(f'{x}{y}'.encode()).hexdigest()[:2] != "ff":
   y += 1
print(f'The solution is y = {y}')
