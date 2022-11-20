`

meal = input("Which meal of the day do you want data for: ")
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

food_items_updated = list(dict.fromkeys(food_items))

print(food_items_updated)

"""
for item in food_items_updated:
    response = api.visualize_recipe_nutrition(item, 1)
    print(response.json())
"""

