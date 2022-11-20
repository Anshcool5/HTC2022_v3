def bmi(weight, height):  # Calculates the Body Mass Index
    height = height*0.01
    return round(weight/(height*height), 1)


def bfp(weight, height, gender, age):  # Calculates the Body Fat Percentge
    BMI = bmi(weight, height)
    if gender == "M":
        return(round(1.20*BMI+(0.23*age)-16.2), (round(1.20*BMI+(0.23*age)-16.2)/100)*weight, round(weight-(round(1.20*BMI+(0.23*age)-16.2)/100)*weight))
    elif gender == "F":
        return (round(1.20*BMI+(0.23*age)-5.4), round(weight-(round(1.20*BMI+(0.23*age)-5.4)/100)*weight))


def bmr(gender, age, weight, height):  # Calculates the Basal Metabolism Rate
    if gender == "M":
        return(round((10*weight)+(6.25*height)-(5*age)+5))  # Mifflin-St Jeor Equation
    elif gender == "F":
        return (round((10*weight)+(6.25*height)-(5*age)-161))  # Mifflin-St Jeor Equation


def main():
    gender = input("Enter yout gender (M/F): ")
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (numerical value only in lbs or kg): "))
    unit_w = input("Enter your chosen unit (lbs or kg): ")
    height = float(input("Enter your height (numerical value only in inches or cm): "))
    unit_h = input("Enter your chosen unit (inches or cm): ")
    activity = input("Enter your activity level (Sedentary/Light/Moderate/Active/Very Active): ")
    goal = input("How do you want to maintain your current weight (maintain/lose/gain): ")
    if unit_w == "lbs" :
        weight = float(weight)*0.453592  # Converts weight in lbs to kg
    if unit_h == "inches":
        height = float(height)*2.54  # Converts the height in inches to cm
    print(f"Your BMI is: {bmi(weight, height)}")
    BFP = bfp(weight, height, gender, age)
    print(f'Your Body Fat Percentage is: {BFP[0]}%')
    BMR = bmr(gender, age, weight, height)
    print(f"Your Basal Metabolism Rate is: {BMR}")
    print(f"Your Fat mass is: {BFP[1]}kg")
    print(f"Your Lean body mass is: {BFP[2]}kg")

    activity_level = ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
    value = [1.2, 1.375, 1.55, 1.725, 1.9]
    for i in range(len(activity_level)):
        if activity == activity_level[i]:
            if goal == "maintain":
                AMR = round(BMR*value[i])                
            elif goal == "lose":
                AMR = round(BMR*value[i-1])
            elif goal == "gain":
                AMR = round(BMR*value[i+1])
    print(f"You should consume {AMR} calories on a daily basis.")
    print(f"You need {round(0.2*AMR)} grams of Protein on a daily basis.")
    print(f"You need {round(0.55*AMR)} grams of Carbohydrates on a daily basis.")
    print(f"You need {round(0.25*AMR)} grams of Fat on a daily basis.")
    
main()

