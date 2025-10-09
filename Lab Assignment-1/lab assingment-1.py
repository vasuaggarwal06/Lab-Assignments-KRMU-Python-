nmeals=int(input("enter no of meals:"))
foods=[]    
calories=[]
for i in range(1,nmeals+1):
    foodname=input("enter your meal:")
    calorie=int(input("enter calories:"))
    foods.append(foodname)
    calories.append(calorie)

Total_calories=(sum(calories))

if Total_calories>2200:
    print("!!Too much calories for today!!")

print("Meal name      |     calories")

for i in range(1,nmeals+1):
    print(f'{foods[i-1]}            {calories[i-1]}')

average=sum(calories)/len(calories)
print(f'Average:          {average}')
print(f'Total:             {sum(calories)}')
