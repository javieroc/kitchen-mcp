BASE_URL="http://localhost:8001"
TOKEN="eyJhbGciOiJFUzI1NiIsImtpZCI6IjE0MmNiZTkwLTYyYzEtNDYwYy1hZWM0LTJlYWM3OTFkMjViNiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3R4Zm5pb2ZpZ2R5aWp1YXh2ZmFhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJmMzEzZDg1YS05MDRjLTRhZGQtOWU4Ni01YWNiYjMzMWFlZDgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzc1MzM3NjczLCJpYXQiOjE3NzUzMzQwNzMsImVtYWlsIjoiZmVycm94aWRvQGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzc1MzM0MDczfV0sInNlc3Npb25faWQiOiJhZDEyNThmMS1hNmYyLTQ4MzYtODk5YS01Y2EwYjAzMWRmOTkiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.fQy32GZJeTA1a_pzllP825l1atmDy5oL4s_deI24zq8Xkwnfgi8X1cBTcvMaRDYgWq2tpmZZAP4HeNjwPkev9g"

recipes='[
{"name":"Overnight Oats","description":"Healthy breakfast with oats and milk","ingredients":[{"name":"Oats","quantity_used":100},{"name":"Milk","quantity_used":200},{"name":"Honey","quantity_used":10}]},
{"name":"Avocado Toast","description":"Toasted bread with smashed avocado","ingredients":[{"name":"Bread","quantity_used":2},{"name":"Avocado","quantity_used":1},{"name":"Lemon","quantity_used":1}]},
{"name":"Yogurt Parfait","description":"Yogurt layered with fruit and granola","ingredients":[{"name":"Yogurt","quantity_used":200},{"name":"Granola","quantity_used":50},{"name":"Berries","quantity_used":100}]},
{"name":"Scrambled Eggs","description":"Quick scrambled eggs breakfast","ingredients":[{"name":"Egg","quantity_used":3},{"name":"Butter","quantity_used":10},{"name":"Salt","quantity_used":1}]},
{"name":"Breakfast Quesadilla","description":"Egg and cheese tortilla breakfast","ingredients":[{"name":"Egg","quantity_used":2},{"name":"Tortilla","quantity_used":1},{"name":"Cheese","quantity_used":50}]},

{"name":"Chicken Salad","description":"Healthy chicken salad lunch","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Lettuce","quantity_used":100},{"name":"Olive Oil","quantity_used":10}]},
{"name":"Tuna Sandwich","description":"Classic tuna sandwich","ingredients":[{"name":"Tuna","quantity_used":120},{"name":"Bread","quantity_used":2},{"name":"Mayonnaise","quantity_used":20}]},
{"name":"Veggie Stir Fry","description":"Vegetables stir fried with soy sauce","ingredients":[{"name":"Broccoli","quantity_used":100},{"name":"Carrot","quantity_used":50},{"name":"Soy Sauce","quantity_used":10}]},
{"name":"Rice Bowl","description":"Rice with vegetables and protein","ingredients":[{"name":"Rice","quantity_used":150},{"name":"Chicken","quantity_used":120},{"name":"Vegetables","quantity_used":100}]},
{"name":"Pasta Salad","description":"Cold pasta with vegetables","ingredients":[{"name":"Pasta","quantity_used":150},{"name":"Tomato","quantity_used":80},{"name":"Olive Oil","quantity_used":10}]},

{"name":"Spaghetti Bolognese","description":"Classic Italian pasta dish","ingredients":[{"name":"Pasta","quantity_used":150},{"name":"Beef","quantity_used":120},{"name":"Tomato Sauce","quantity_used":100}]},
{"name":"Chicken Fajitas","description":"Grilled chicken with peppers","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Bell Pepper","quantity_used":80},{"name":"Tortilla","quantity_used":2}]},
{"name":"Beef Tacos","description":"Mexican tacos with beef","ingredients":[{"name":"Beef","quantity_used":120},{"name":"Tortilla","quantity_used":3},{"name":"Cheese","quantity_used":50}]},
{"name":"Mac and Cheese","description":"Creamy pasta with cheese","ingredients":[{"name":"Pasta","quantity_used":150},{"name":"Cheese","quantity_used":100},{"name":"Milk","quantity_used":100}]},
{"name":"BBQ Chicken Pizza","description":"Pizza with BBQ chicken","ingredients":[{"name":"Dough","quantity_used":200},{"name":"Chicken","quantity_used":100},{"name":"BBQ Sauce","quantity_used":50}]},

{"name":"Egg Muffins","description":"Baked egg breakfast cups","ingredients":[{"name":"Egg","quantity_used":4},{"name":"Cheese","quantity_used":50},{"name":"Spinach","quantity_used":50}]},
{"name":"Omelette","description":"Classic egg omelette","ingredients":[{"name":"Egg","quantity_used":3},{"name":"Cheese","quantity_used":40},{"name":"Milk","quantity_used":30}]},
{"name":"French Toast","description":"Sweet breakfast toast","ingredients":[{"name":"Bread","quantity_used":2},{"name":"Egg","quantity_used":2},{"name":"Milk","quantity_used":100}]},
{"name":"Pancakes","description":"Fluffy pancakes","ingredients":[{"name":"Flour","quantity_used":150},{"name":"Milk","quantity_used":200},{"name":"Egg","quantity_used":2}]},
{"name":"Chia Pudding","description":"Healthy chia breakfast","ingredients":[{"name":"Chia Seeds","quantity_used":50},{"name":"Milk","quantity_used":200},{"name":"Honey","quantity_used":10}]},

{"name":"Chicken Rice","description":"Simple chicken and rice","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Rice","quantity_used":150},{"name":"Salt","quantity_used":5}]},
{"name":"Beef Stroganoff","description":"Creamy beef pasta","ingredients":[{"name":"Beef","quantity_used":150},{"name":"Pasta","quantity_used":150},{"name":"Cream","quantity_used":100}]},
{"name":"Lasagna","description":"Layered pasta with meat","ingredients":[{"name":"Pasta","quantity_used":200},{"name":"Beef","quantity_used":150},{"name":"Cheese","quantity_used":100}]},
{"name":"Chicken Alfredo","description":"Pasta with creamy sauce","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Pasta","quantity_used":150},{"name":"Cream","quantity_used":100}]},
{"name":"Ravioli","description":"Stuffed pasta","ingredients":[{"name":"Ravioli","quantity_used":200},{"name":"Tomato Sauce","quantity_used":100}]},

{"name":"Grilled Chicken","description":"Simple grilled chicken","ingredients":[{"name":"Chicken","quantity_used":200},{"name":"Olive Oil","quantity_used":10},{"name":"Salt","quantity_used":5}]},
{"name":"Steak","description":"Grilled beef steak","ingredients":[{"name":"Beef","quantity_used":250},{"name":"Salt","quantity_used":5}]},
{"name":"Pot Roast","description":"Slow cooked beef","ingredients":[{"name":"Beef","quantity_used":300},{"name":"Carrot","quantity_used":100},{"name":"Potato","quantity_used":150}]},
{"name":"Shepherd Pie","description":"Meat and mashed potatoes","ingredients":[{"name":"Beef","quantity_used":150},{"name":"Potato","quantity_used":200},{"name":"Carrot","quantity_used":50}]},
{"name":"Chicken Soup","description":"Warm chicken soup","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Water","quantity_used":500},{"name":"Carrot","quantity_used":50}]},

{"name":"Chili","description":"Spicy bean stew","ingredients":[{"name":"Beans","quantity_used":200},{"name":"Beef","quantity_used":100},{"name":"Tomato","quantity_used":100}]},
{"name":"Beef Stew","description":"Slow cooked beef stew","ingredients":[{"name":"Beef","quantity_used":200},{"name":"Potato","quantity_used":150},{"name":"Carrot","quantity_used":100}]},
{"name":"Quesadillas","description":"Cheese filled tortillas","ingredients":[{"name":"Tortilla","quantity_used":2},{"name":"Cheese","quantity_used":100}]},
{"name":"Enchiladas","description":"Rolled tortillas with filling","ingredients":[{"name":"Tortilla","quantity_used":3},{"name":"Chicken","quantity_used":150},{"name":"Sauce","quantity_used":100}]},
{"name":"Hamburger","description":"Classic burger","ingredients":[{"name":"Beef","quantity_used":150},{"name":"Bread","quantity_used":1},{"name":"Cheese","quantity_used":50}]},

{"name":"Fried Rice","description":"Rice stir fried with eggs","ingredients":[{"name":"Rice","quantity_used":150},{"name":"Egg","quantity_used":2},{"name":"Soy Sauce","quantity_used":10}]},
{"name":"Shrimp Pasta","description":"Pasta with shrimp","ingredients":[{"name":"Shrimp","quantity_used":120},{"name":"Pasta","quantity_used":150},{"name":"Garlic","quantity_used":10}]},
{"name":"Tofu Stir Fry","description":"Vegetarian stir fry","ingredients":[{"name":"Tofu","quantity_used":150},{"name":"Vegetables","quantity_used":150},{"name":"Soy Sauce","quantity_used":10}]},
{"name":"Chicken Sandwich","description":"Grilled chicken sandwich","ingredients":[{"name":"Chicken","quantity_used":150},{"name":"Bread","quantity_used":2},{"name":"Lettuce","quantity_used":50}]},
{"name":"Salad Bowl","description":"Mixed vegetable salad","ingredients":[{"name":"Lettuce","quantity_used":100},{"name":"Tomato","quantity_used":80},{"name":"Olive Oil","quantity_used":10}]},

{"name":"Egg Salad","description":"Egg based salad","ingredients":[{"name":"Egg","quantity_used":3},{"name":"Mayonnaise","quantity_used":20},{"name":"Mustard","quantity_used":5}]},
{"name":"Quiche","description":"Savory egg pie","ingredients":[{"name":"Egg","quantity_used":4},{"name":"Cheese","quantity_used":100},{"name":"Milk","quantity_used":100}]},
{"name":"Frittata","description":"Italian egg dish","ingredients":[{"name":"Egg","quantity_used":4},{"name":"Vegetables","quantity_used":100}]},
{"name":"Breakfast Burrito","description":"Egg wrap with fillings","ingredients":[{"name":"Egg","quantity_used":3},{"name":"Tortilla","quantity_used":1},{"name":"Cheese","quantity_used":50}]},
{"name":"Hash Browns","description":"Fried potato breakfast","ingredients":[{"name":"Potato","quantity_used":200},{"name":"Oil","quantity_used":20}]}
]'

echo "$recipes" | jq -c '.[]' | while read recipe; do
  curl -X POST "$BASE_URL/recipes" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$recipe"
done
