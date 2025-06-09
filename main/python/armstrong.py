lower_range = int(input("Enter lower Range:"))
upper_range = int(input("Enter upper Range:"))

def is_arm_strong(number):
    num = str(number)
    order = len(num)
    sum = 0
    for a in num:
        sum += int(a) ** order
    if sum == number:
        print(f'{number} is a armstrong number.')
        
for i in range(lower_range,upper_range+1):
    is_arm_strong(i)
