from flask import Flask, flash, redirect, render_template, \
     request, url_for
import requests
import noms

client = noms.Client("SsIueuWnAo3d0kqKGdbxlY45vRaWoyE2FW4kCcrC")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'name':'breakfast'}, {'name':'lunch'}, {'name':'dinner'}], gen=["Male", "Female"],
        w=["kg", "lbs"], h=["inches", "cm"], a=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
        g=["maintain", "lose", "gain"])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    meal=str(select)
    s = request.form.get('age')
    age = int(s)
    e = request.form.get('gen_select')
    gender = str(e)
    b = request.form.get('weight')
    weight = int(b)
    l = request.form.get('wei_select')
    unit_w = str(l)
    d = request.form.get('height')
    height = int(d)
    c = request.form.get('hei_select')
    unit_h = str(c)
    t = request.form.get('a_select')
    activity = str(t)
    f = request.form.get('g_select')
    goal = str(f)
    if meal == "breakfast":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=879&fulfillmentMethod="
    elif meal == "lunch":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=880&fulfillmentMethod="
    elif meal == "dinner":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=881&fulfillmentMethod="
    res = requests.get(url)
    data = res.json()
    food_items = []
    for element in data["Menu"]["MenuProducts"]:
        food_items.append(element["Product"]["MarketingName"])
    if unit_w == "lbs" :
        weight = float(weight)*0.453592  # Converts weight in lbs to kg
    if unit_h == "inches":
        height = float(height)*2.54
    height = height*0.01
    BMI = round(weight/(height*height), 1)
    if gender == "Male":
        BFP = round(1.20*BMI+(0.23*age)-16.2)
        fat_mass = (round(1.20*BMI+(0.23*age)-16.2)/100)*weight
        lean_body_mass = round(weight-(round(1.20*BMI+(0.23*age)-16.2)/100)*weight)
        BMR = round((10*weight)+(6.25*height)-(5*age)+5)
    elif gender == "Female":
        BFP = round(1.20*BMI+(0.23*age)-5.4)
        fat_mass = round(weight-(round(1.20*BMI+(0.23*age)-5.4)/100)*weight)
        BMR = round((10*weight)+(6.25*height)-(5*age)-161)
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
    names_of_food = list(dict.fromkeys(food_items))
    return render_template("menu.html", food_items_updated = names_of_food, Cal = AMR, Prot = round(0.2*AMR), Carb = round(0.55*AMR), Fat = round(0.25*AMR))

@app.route("/nutrition" , methods=['GET', 'POST'])
def nutrition():
    select = request.form.get('comp_select')
    meal=str(select)
    if meal == "breakfast":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=879&fulfillmentMethod="
    elif meal == "lunch":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=880&fulfillmentMethod="
    elif meal == "dinner":
        url = "https://ualberta.campusdish.com/api/menu/GetMenus?locationId=5252&storeIds=&mode=Daily&date=11/19/2022&time=&periodId=881&fulfillmentMethod="
    res = requests.get(url)
    data = res.json()
    food_items = []
    for element in data["Menu"]["MenuProducts"]:
        food_items.append(element["Product"]["MarketingName"])
    names_of_food = list(dict.fromkeys(food_items))
    tot_cal = 0
    tot_prot = 0
    tot_carb = 0
    tot_fat = 0
    ans=[tot_prot, tot_fat, tot_carb, tot_cal]
    meal_res = []
    for item in names_of_food:
        while ans[3] <= 500:
            food_dict_daily = {}
            results = client.search_query(item)
            food_dict = results.json
            try:
                res = food_dict['items'][0]
            except TypeError:
                break

            abc = res['fdcId']
            food_dict_daily[abc] = 50


            food_objs = client.get_foods(food_dict_daily)
            ml = noms.Meal(food_objs)

            r = noms.report(ml)
            val_list = []
            for i in r:
                for i['name'] in ['Protein', 'Fat', 'Carbs', 'Calories']:
                    val_list.append(i['value'])
                    break
            for j in range(0, 4):
                ans[j] += val_list[j]
            meal_res.append(item)
            print(ans[3])
            break
    return render_template("result.html", rec_meal = meal_res)


if __name__=='__main__':
    app.run(debug=True)