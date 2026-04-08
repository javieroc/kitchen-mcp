BASE_URL="http://localhost:8001"


tmpfile=$(mktemp /tmp/kitchen_seed_XXXXXX.json)
trap "rm -f \"$tmpfile\"" EXIT

cat > "$tmpfile" << 'RECIPES_EOF'
[
  {
    "name": "Overnight Oats",
    "description": "1. Add rolled oats, chia seeds, and vanilla extract to a jar or container.\n2. Pour in milk and mix well to combine.\n3. Fold in Greek yogurt and drizzle in honey. Stir until fully incorporated.\n4. Cover and refrigerate overnight or for at least 4 hours.\n5. In the morning, give it a stir — it should be thick and creamy.\n6. Add your favourite toppings like fresh fruit, nuts, or an extra drizzle of honey. Serve cold.",
    "category": "breakfast",
    "yield_amount": 1,
    "yield_unit": "portion",
    "image_url": "https://www.themealdb.com/images/media/meals/sng9bm1765320170.jpg",
    "ingredients": [
      {"name": "Rolled Oats", "quantity_used": 80, "unit_of_measure": "g"},
      {"name": "Milk", "quantity_used": 200, "unit_of_measure": "ml"},
      {"name": "Greek Yogurt", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Chia Seeds", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Honey", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Vanilla Extract", "quantity_used": 2.5, "unit_of_measure": "ml"}
    ]
  },
  {
    "name": "Scrambled Eggs",
    "description": "1. Crack eggs into a bowl, add milk, salt, and pepper, then beat until fully combined.\n2. Melt butter in a non-stick pan over medium-low heat.\n3. Pour in the egg mixture and let it sit undisturbed for 20 seconds.\n4. Using a spatula, gently fold the eggs from the edges toward the center in slow, deliberate strokes.\n5. Remove from heat while the eggs still look slightly underdone — residual heat finishes the cooking.\n6. Plate immediately and serve with toast or fresh herbs.",
    "category": "breakfast",
    "yield_amount": 1,
    "yield_unit": "portion",
    "image_url": "https://www.themealdb.com/images/media/meals/1550440197.jpg",
    "ingredients": [
      {"name": "Large Eggs", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Unsalted Butter", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Whole Milk", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Pancakes",
    "description": "1. Whisk together flour, sugar, baking powder, and salt in a large bowl.\n2. In a separate bowl, whisk milk, melted butter, and egg together.\n3. Pour wet ingredients into dry and stir gently until just combined — lumps are fine, do not over-mix.\n4. Heat a non-stick skillet over medium heat and lightly grease.\n5. Pour about 60ml of batter per pancake onto the skillet.\n6. Cook until bubbles form on the surface and the edges look set, about 2–3 minutes.\n7. Flip and cook for another 1–2 minutes until golden.\n8. Serve warm with maple syrup and butter.",
    "category": "breakfast",
    "yield_amount": 8,
    "yield_unit": "pancakes",
    "image_url": "https://www.themealdb.com/images/media/meals/rwuyqx1511383174.jpg",
    "ingredients": [
      {"name": "All-Purpose Flour", "quantity_used": 125, "unit_of_measure": "g"},
      {"name": "Granulated Sugar", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Baking Powder", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Whole Milk", "quantity_used": 240, "unit_of_measure": "ml"},
      {"name": "Unsalted Butter", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Large Egg", "quantity_used": 1, "unit_of_measure": "unit"}
    ]
  },
  {
    "name": "French Toast",
    "description": "1. In a shallow bowl, whisk together eggs, milk, cinnamon, vanilla extract, and salt until well combined.\n2. Heat butter in a large skillet over medium heat.\n3. Dip each bread slice into the egg mixture, letting it soak for about 10 seconds per side.\n4. Place soaked bread in the pan and cook for 2–3 minutes per side until golden brown.\n5. Work in batches if needed, adding more butter between batches.\n6. Serve immediately with powdered sugar, maple syrup, or fresh fruit.",
    "category": "breakfast",
    "yield_amount": 4,
    "yield_unit": "slices",
    "image_url": "https://www.themealdb.com/images/media/meals/iydbwy1763816111.jpg",
    "ingredients": [
      {"name": "Large Eggs", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Whole Milk", "quantity_used": 120, "unit_of_measure": "ml"},
      {"name": "Ground Cinnamon", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Vanilla Extract", "quantity_used": 5, "unit_of_measure": "ml"},
      {"name": "Bread Slices", "quantity_used": 4, "unit_of_measure": "unit"},
      {"name": "Unsalted Butter", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Avocado Toast",
    "description": "1. Toast bread slices until golden and crisp.\n2. Halve the avocado, remove the pit, and scoop the flesh into a bowl.\n3. Add lemon juice, salt, and black pepper. Mash with a fork to your desired consistency.\n4. Drizzle olive oil into the mash and stir to combine.\n5. Spoon the avocado mixture evenly onto the toasted bread.\n6. Finish with red pepper flakes and an extra drizzle of olive oil. Serve immediately.",
    "category": "breakfast",
    "yield_amount": 2,
    "yield_unit": "slices",
    "image_url": "https://www.themealdb.com/images/media/meals/1549542994.jpg",
    "ingredients": [
      {"name": "Ripe Avocado", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Bread Slices", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Lemon Juice", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 1, "unit_of_measure": "g"},
      {"name": "Red Pepper Flakes", "quantity_used": 0.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Greek Salad",
    "description": "1. Halve or quarter the cherry tomatoes and place in a large bowl.\n2. Dice the cucumber into bite-sized chunks and add to the bowl.\n3. Slice the green bell pepper into strips and thinly slice the red onion; add both.\n4. Scatter in the kalamata olives.\n5. In a small bowl, whisk together olive oil, red wine vinegar, dried oregano, salt, and pepper to make the dressing.\n6. Pour the dressing over the vegetables and toss gently.\n7. Top with crumbled or sliced feta cheese — do not toss after adding feta.\n8. Serve immediately or refrigerate for up to 30 minutes.",
    "category": "lunch",
    "yield_amount": 2,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/k29viq1585565980.jpg",
    "ingredients": [
      {"name": "Cherry Tomatoes", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "English Cucumber", "quantity_used": 300, "unit_of_measure": "g"},
      {"name": "Green Bell Pepper", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Red Onion", "quantity_used": 50, "unit_of_measure": "g"},
      {"name": "Kalamata Olives", "quantity_used": 80, "unit_of_measure": "g"},
      {"name": "Feta Cheese", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 45, "unit_of_measure": "ml"},
      {"name": "Red Wine Vinegar", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Dried Oregano", "quantity_used": 5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Chicken Caesar Wrap",
    "description": "1. Slice or shred the cooked chicken breast into bite-sized pieces.\n2. In a bowl, combine romaine lettuce, halved cherry tomatoes, and parmesan cheese.\n3. Drizzle caesar dressing over the salad and toss to coat evenly.\n4. Warm the tortilla in a dry pan or microwave for 20 seconds until pliable.\n5. Lay the tortilla flat and layer the dressed salad in the center, leaving a 5cm border.\n6. Add sliced chicken and croutons on top. Season with black pepper.\n7. Fold in the sides of the tortilla, then roll tightly from the bottom up.\n8. Slice diagonally and serve.",
    "category": "lunch",
    "yield_amount": 1,
    "yield_unit": "wrap",
    "image_url": "https://www.themealdb.com/images/media/meals/prrirc1763781360.jpg",
    "ingredients": [
      {"name": "Cooked Chicken Breast", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Romaine Lettuce", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Cherry Tomatoes", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Parmesan Cheese", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Caesar Dressing", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Croutons", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Tortilla Wrap", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Black Pepper", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Caprese Sandwich",
    "description": "1. Slice the ciabatta roll in half and lightly toast the cut sides under a broiler or in a dry pan.\n2. Slice fresh mozzarella and ripe tomato into even rounds.\n3. Drizzle olive oil over the bottom half of the ciabatta.\n4. Layer mozzarella and tomato slices alternately on the bread.\n5. Season with salt and black pepper.\n6. Tuck fresh basil leaves between the mozzarella and tomato layers.\n7. Drizzle balsamic vinegar over the filling.\n8. Place the top half of the ciabatta on, press gently, and serve immediately.",
    "category": "lunch",
    "yield_amount": 1,
    "yield_unit": "sandwich",
    "image_url": "https://www.themealdb.com/images/media/meals/j80gmw1764372176.jpg",
    "ingredients": [
      {"name": "Fresh Mozzarella", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Ripe Tomato", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Fresh Basil", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Ciabatta Roll", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Balsamic Vinegar", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Beef Tacos",
    "description": "1. Dice the onion and mince the garlic.\n2. Brown ground beef in a large skillet over medium-high heat, breaking it up as it cooks. Drain excess fat.\n3. Add onion and garlic; cook for 3 minutes until softened.\n4. Stir in chili powder and cumin; cook for 1 minute until fragrant.\n5. Pour in tomato sauce and chicken broth. Simmer uncovered for 8–10 minutes until the sauce thickens.\n6. Season with salt and pepper.\n7. Warm taco shells according to packet instructions.\n8. Fill each shell with the beef mixture and top with shredded cheese, lettuce, diced tomato, and sour cream.",
    "category": "lunch",
    "yield_amount": 8,
    "yield_unit": "tacos",
    "image_url": "https://www.themealdb.com/images/media/meals/uvuyxu1503067369.jpg",
    "ingredients": [
      {"name": "Ground Beef", "quantity_used": 450, "unit_of_measure": "g"},
      {"name": "Onion", "quantity_used": 80, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Chili Powder", "quantity_used": 7.5, "unit_of_measure": "g"},
      {"name": "Ground Cumin", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Tomato Sauce", "quantity_used": 120, "unit_of_measure": "ml"},
      {"name": "Chicken Broth", "quantity_used": 120, "unit_of_measure": "ml"},
      {"name": "Taco Shells", "quantity_used": 8, "unit_of_measure": "unit"},
      {"name": "Shredded Cheddar Cheese", "quantity_used": 120, "unit_of_measure": "g"},
      {"name": "Shredded Lettuce", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Diced Tomato", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Sour Cream", "quantity_used": 60, "unit_of_measure": "ml"}
    ]
  },
  {
    "name": "Beef Burger",
    "description": "1. In a large bowl, combine ground beef, breadcrumbs, egg, Worcestershire sauce, onion powder, garlic powder, mustard, salt, and pepper. Mix gently — do not over-mix.\n2. Divide into 4 equal portions and shape into patties about 2cm thick. Press a shallow indent in the center of each to prevent bulging.\n3. Heat a grill or skillet over high heat.\n4. Cook patties for 3–4 minutes per side for medium doneness.\n5. Toast burger buns on the grill for 1 minute.\n6. Assemble with your favourite toppings such as lettuce, tomato, cheese, and condiments.",
    "category": "lunch",
    "yield_amount": 4,
    "yield_unit": "burgers",
    "image_url": "https://www.themealdb.com/images/media/meals/lgmnff1763789847.jpg",
    "ingredients": [
      {"name": "Ground Beef", "quantity_used": 900, "unit_of_measure": "g"},
      {"name": "Panko Breadcrumbs", "quantity_used": 40, "unit_of_measure": "g"},
      {"name": "Large Egg", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Worcestershire Sauce", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Onion Powder", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Garlic Powder", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Dijon Mustard", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Burger Buns", "quantity_used": 4, "unit_of_measure": "unit"}
    ]
  },
  {
    "name": "Spaghetti Carbonara",
    "description": "1. Bring a large pot of heavily salted water to a boil and cook spaghetti until al dente. Reserve 200ml of pasta cooking water before draining.\n2. While pasta cooks, cut guanciale into cubes and fry in a cold pan over medium heat until crispy and the fat has rendered. Remove from heat.\n3. In a bowl, whisk together eggs, egg yolk, finely grated pecorino, and plenty of black pepper.\n4. Add the hot drained pasta to the pan with the guanciale off the heat.\n5. Pour the egg and cheese mixture over the pasta and toss vigorously, adding pasta water a splash at a time until a creamy, glossy sauce forms — residual heat cooks the eggs without scrambling them.\n6. Serve immediately with extra pecorino and black pepper.",
    "category": "dinner",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg",
    "ingredients": [
      {"name": "Spaghetti", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Guanciale", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Large Eggs", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Egg Yolks", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Pecorino Romano Cheese", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 10, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Chicken Stir Fry",
    "description": "1. Slice chicken breast into thin strips. Whisk together soy sauce, honey, chicken broth, rice wine vinegar, and cornstarch to make the sauce.\n2. Mince garlic and ginger. Cut broccoli into florets; slice bell pepper and carrot into thin strips.\n3. Heat oil in a wok over high heat until smoking.\n4. Add chicken and cook undisturbed for 2 minutes, then stir-fry for 2 more minutes until cooked through. Remove and set aside.\n5. In the same pan, add a little more oil and stir-fry the vegetables for 3–4 minutes until tender-crisp.\n6. Add garlic and ginger; cook for 30 seconds.\n7. Return chicken, pour in the sauce, and toss until the sauce thickens and coats everything, about 1–2 minutes.\n8. Serve over steamed rice.",
    "category": "dinner",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/rwvw8q1765660071.jpg",
    "ingredients": [
      {"name": "Boneless Chicken Breast", "quantity_used": 450, "unit_of_measure": "g"},
      {"name": "Broccoli Florets", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Bell Pepper", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Carrot", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Chicken Broth", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Soy Sauce", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Honey", "quantity_used": 22.5, "unit_of_measure": "ml"},
      {"name": "Cornstarch", "quantity_used": 7.5, "unit_of_measure": "g"},
      {"name": "Rice Wine Vinegar", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Fresh Ginger", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Canola Oil", "quantity_used": 30, "unit_of_measure": "ml"}
    ]
  },
  {
    "name": "Mushroom Risotto",
    "description": "1. Heat vegetable broth in a saucepan and keep warm on low heat throughout.\n2. In a large heavy pan, heat olive oil and half the butter over medium heat. Sauté diced shallot until soft, about 3 minutes. Add minced garlic and thyme; cook 1 minute.\n3. Add arborio rice and toast, stirring constantly, for 2 minutes until the edges turn translucent.\n4. Pour in white wine and stir until completely absorbed.\n5. Add warm broth one ladle at a time, stirring frequently and waiting until each addition is absorbed before adding the next. Continue for 18–20 minutes until rice is creamy and al dente.\n6. Meanwhile, in a separate pan, sauté sliced mushrooms in the remaining butter over high heat until browned, about 5 minutes.\n7. Fold mushrooms and grated parmesan into the risotto. Season with salt and pepper.\n8. Serve immediately in warm bowls.",
    "category": "dinner",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/xxrxux1503070723.jpg",
    "ingredients": [
      {"name": "Arborio Rice", "quantity_used": 300, "unit_of_measure": "g"},
      {"name": "Fresh Mushrooms", "quantity_used": 450, "unit_of_measure": "g"},
      {"name": "Vegetable Broth", "quantity_used": 1500, "unit_of_measure": "ml"},
      {"name": "Unsalted Butter", "quantity_used": 60, "unit_of_measure": "g"},
      {"name": "Shallot", "quantity_used": 50, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Fresh Thyme", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "White Wine", "quantity_used": 120, "unit_of_measure": "ml"},
      {"name": "Parmesan Cheese", "quantity_used": 80, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Grilled Salmon",
    "description": "1. Pat salmon fillets dry with paper towels. Mix olive oil, lemon juice, lemon zest, minced garlic, and chopped fresh dill.\n2. Season both sides of the salmon with salt and pepper. Brush generously with the lemon-dill marinade.\n3. Preheat a grill or grill pan to medium-high heat and oil the grates.\n4. Place salmon skin-side down and grill without moving for 4–5 minutes until the flesh turns opaque halfway up the sides.\n5. Carefully flip and cook for another 2–3 minutes until cooked through but still moist in the center.\n6. In the last minute, add a knob of butter on top and let it melt over the fish.\n7. Serve immediately with lemon wedges and remaining fresh dill.",
    "category": "dinner",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/ikizdm1763760862.jpg",
    "ingredients": [
      {"name": "Salmon Fillets", "quantity_used": 600, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Lemon Juice", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Lemon Zest", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Fresh Dill", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Unsalted Butter", "quantity_used": 20, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Beef Stew",
    "description": "1. Cut beef chuck into 3cm cubes and season generously with salt and pepper. Dice onion, carrot, celery, and potato. Mince garlic.\n2. Heat olive oil in a large Dutch oven over high heat. Sear beef in batches until browned on all sides, about 4 minutes per batch. Remove and set aside.\n3. Reduce heat to medium. Add onion, carrot, and celery; cook for 5 minutes. Add garlic; cook 1 minute.\n4. Stir in tomato paste and cook for 2 minutes. Pour in red wine and scrape up any browned bits from the bottom.\n5. Return beef to the pot, add beef broth and dried thyme. Bring to a boil, then reduce to a low simmer.\n6. Cover and cook for 1.5 hours. Add potato chunks and continue cooking for 30 more minutes until beef is tender.\n7. Taste and adjust seasoning. Serve with crusty bread.",
    "category": "dinner",
    "yield_amount": 6,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/ntafxw1763586291.jpg",
    "ingredients": [
      {"name": "Beef Chuck", "quantity_used": 900, "unit_of_measure": "g"},
      {"name": "Onion", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Carrot", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Celery", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Yukon Gold Potato", "quantity_used": 300, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Tomato Paste", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Beef Broth", "quantity_used": 500, "unit_of_measure": "ml"},
      {"name": "Red Wine", "quantity_used": 250, "unit_of_measure": "ml"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Dried Thyme", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Pad Thai",
    "description": "1. Soak rice noodles in cold water for 30 minutes until pliable, then drain.\n2. Whisk together fish sauce, tamarind paste, palm sugar, peanut butter, rice vinegar, and sriracha to make the sauce.\n3. Peel and devein shrimp. Mince garlic.\n4. Heat peanut oil in a wok over high heat. Stir-fry shrimp for 2 minutes until pink. Push to the side.\n5. Add garlic; cook 30 seconds. Push everything to the side, crack in the egg, and scramble until just set.\n6. Add drained noodles and pour in the sauce. Toss everything together over high heat for 2–3 minutes until noodles absorb the sauce.\n7. Add bean sprouts; toss for 30 seconds.\n8. Serve topped with sliced scallions and crushed roasted peanuts. Garnish with lime wedges.",
    "category": "dinner",
    "yield_amount": 2,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/rg9ze01763479093.jpg",
    "ingredients": [
      {"name": "Rice Noodles", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Large Shrimp", "quantity_used": 300, "unit_of_measure": "g"},
      {"name": "Fish Sauce", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Tamarind Paste", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Palm Sugar", "quantity_used": 50, "unit_of_measure": "g"},
      {"name": "Peanut Butter", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Rice Vinegar", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Sriracha", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Large Egg", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Peanut Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Bean Sprouts", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Scallion", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Roasted Peanuts", "quantity_used": 40, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Spinach and Feta Stuffed Chicken",
    "description": "1. Preheat oven to 200°C / 400°F. Wilt fresh spinach in a pan until completely collapsed, then squeeze out all excess water and roughly chop.\n2. In a bowl, combine wilted spinach, crumbled feta, softened cream cheese, minced garlic, sliced scallions, chopped dill, nutmeg, salt, and pepper. Mix well.\n3. Cut a deep pocket into the side of each chicken breast without cutting all the way through.\n4. Stuff each pocket generously with the filling and secure the opening with toothpicks.\n5. Season the outside with salt and pepper.\n6. Heat olive oil in an oven-safe skillet over high heat. Sear chicken for 3 minutes per side until golden.\n7. Transfer the skillet to the oven and bake for 18–20 minutes until cooked through.\n8. Rest for 5 minutes, remove toothpicks, and serve.",
    "category": "dinner",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/pk8wtn1763758591.jpg",
    "ingredients": [
      {"name": "Boneless Chicken Breast", "quantity_used": 600, "unit_of_measure": "g"},
      {"name": "Fresh Spinach", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Feta Cheese", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Cream Cheese", "quantity_used": 50, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Scallion", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Fresh Dill", "quantity_used": 7.5, "unit_of_measure": "g"},
      {"name": "Nutmeg", "quantity_used": 1, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Quiche Lorraine",
    "description": "1. Make the pastry: rub cold diced butter into flour until it resembles breadcrumbs. Add ice water one tablespoon at a time and mix until the dough just comes together. Shape into a disc, wrap, and refrigerate for 30 minutes.\n2. Preheat oven to 190°C / 375°F. Roll out the dough and line a 23cm tart tin. Blind bake with weights for 15 minutes, remove weights, bake 5 more minutes.\n3. Cook bacon in a pan until crispy. Drain and cool.\n4. Whisk together eggs, milk, and heavy cream until smooth. Season with salt and pepper.\n5. Scatter bacon and grated gruyere evenly over the pastry base.\n6. Pour the egg and cream mixture over the top.\n7. Bake for 30–35 minutes until the custard is just set with a slight wobble in the center.\n8. Cool for at least 15 minutes before slicing. Serve warm or at room temperature.",
    "category": "dinner",
    "yield_amount": 8,
    "yield_unit": "slices",
    "image_url": "https://www.themealdb.com/images/media/meals/ryspuw1511786688.jpg",
    "ingredients": [
      {"name": "All-Purpose Flour", "quantity_used": 180, "unit_of_measure": "g"},
      {"name": "Unsalted Butter", "quantity_used": 90, "unit_of_measure": "g"},
      {"name": "Ice Water", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Large Eggs", "quantity_used": 4, "unit_of_measure": "unit"},
      {"name": "Whole Milk", "quantity_used": 240, "unit_of_measure": "ml"},
      {"name": "Heavy Cream", "quantity_used": 240, "unit_of_measure": "ml"},
      {"name": "Gruyere Cheese", "quantity_used": 112, "unit_of_measure": "g"},
      {"name": "Bacon", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Black Pepper", "quantity_used": 2, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Chicken Caesar Salad",
    "description": "1. Season chicken breast with salt and pepper. Heat a grill pan or skillet over medium-high heat with a little olive oil.\n2. Cook chicken for 5–6 minutes per side until cooked through. Rest for 5 minutes, then slice thinly against the grain.\n3. Make the dressing: whisk together mayonnaise, lemon juice, minced garlic, Worcestershire sauce, anchovy paste, and dijon mustard. Season with salt and pepper.\n4. Tear romaine lettuce into bite-sized pieces and place in a large bowl.\n5. Drizzle dressing over the lettuce and toss to coat evenly.\n6. Add croutons and grated parmesan; toss lightly.\n7. Divide into bowls and top with sliced grilled chicken.\n8. Serve with extra parmesan and a crack of black pepper.",
    "category": "fit",
    "yield_amount": 2,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/pk8wtn1763758591.jpg",
    "ingredients": [
      {"name": "Boneless Chicken Breast", "quantity_used": 300, "unit_of_measure": "g"},
      {"name": "Romaine Lettuce", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Parmesan Cheese", "quantity_used": 40, "unit_of_measure": "g"},
      {"name": "Croutons", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Mayonnaise", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Lemon Juice", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Worcestershire Sauce", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Anchovy Paste", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Dijon Mustard", "quantity_used": 5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Chickpea Curry",
    "description": "1. Dice onion and mince garlic and ginger.\n2. Heat olive oil in a large pan over medium heat. Cook onion for 6–7 minutes until golden and softened.\n3. Add garlic and ginger; cook for 1 minute until fragrant.\n4. Add curry powder, ground cumin, and turmeric. Stir and cook for 1 minute to bloom the spices.\n5. Pour in canned tomatoes; stir well and simmer for 5 minutes until the sauce thickens slightly.\n6. Add drained chickpeas and coconut milk. Bring to a simmer and cook for 15 minutes, stirring occasionally.\n7. Stir in lime juice. Taste and adjust salt and seasoning.\n8. Serve over steamed rice or with warm naan bread, topped with fresh cilantro.",
    "category": "fit",
    "yield_amount": 4,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/sstssx1487349585.jpg",
    "ingredients": [
      {"name": "Canned Chickpeas", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Coconut Milk", "quantity_used": 400, "unit_of_measure": "ml"},
      {"name": "Onion", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Fresh Ginger", "quantity_used": 15, "unit_of_measure": "g"},
      {"name": "Canned Tomatoes", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Curry Powder", "quantity_used": 7.5, "unit_of_measure": "g"},
      {"name": "Ground Cumin", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Turmeric Powder", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Lime Juice", "quantity_used": 15, "unit_of_measure": "ml"},
      {"name": "Fresh Cilantro", "quantity_used": 20, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Lentil Soup",
    "description": "1. Dice onion, carrot, and celery. Mince garlic. Rinse lentils in cold water.\n2. Heat olive oil in a large pot over medium heat. Add onion, carrot, and celery; cook for 7 minutes until softened.\n3. Add garlic, dried oregano, and cumin; cook for 1 minute until fragrant.\n4. Add rinsed lentils, vegetable broth, and canned tomatoes. Stir well and bring to a boil.\n5. Reduce heat, cover, and simmer for 25–30 minutes until lentils are completely tender.\n6. Using an immersion blender, partially blend the soup — blend about half for a thick but textured consistency.\n7. Stir in lemon juice. Season generously with salt.\n8. Serve hot with crusty bread or a swirl of olive oil on top.",
    "category": "fit",
    "yield_amount": 6,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/vpxyqt1511464175.jpg",
    "ingredients": [
      {"name": "Brown Lentils", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Onion", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Carrot", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Celery", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Vegetable Broth", "quantity_used": 1500, "unit_of_measure": "ml"},
      {"name": "Canned Diced Tomatoes", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Dried Oregano", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Dried Cumin", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Lemon Juice", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Salmon Poke Bowl",
    "description": "1. Cook sushi rice according to package instructions. While warm, fold in rice wine vinegar and mirin. Spread on a tray and fan to cool.\n2. Whisk together soy sauce, sesame oil, and mirin for the marinade. Stir in minced garlic and ginger.\n3. Cut salmon into 2cm cubes, add to the marinade, and let sit for 10–15 minutes.\n4. Julienne carrot and cucumber. Slice avocado and scallions.\n5. Divide cooled rice between two bowls.\n6. Arrange marinated salmon, sliced avocado, cucumber, carrot, and scallions in separate sections over the rice.\n7. Spoon any remaining marinade over the bowls.\n8. Finish with toasted sesame seeds and serve immediately.",
    "category": "fit",
    "yield_amount": 2,
    "yield_unit": "bowls",
    "image_url": "https://www.themealdb.com/images/media/meals/ikizdm1763760862.jpg",
    "ingredients": [
      {"name": "Fresh Salmon Fillet", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Sushi Rice", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Soy Sauce", "quantity_used": 45, "unit_of_measure": "ml"},
      {"name": "Rice Wine Vinegar", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Mirin", "quantity_used": 20, "unit_of_measure": "ml"},
      {"name": "Sesame Oil", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Fresh Ginger", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Scallion", "quantity_used": 30, "unit_of_measure": "g"},
      {"name": "Avocado", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Cucumber", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Carrot", "quantity_used": 50, "unit_of_measure": "g"},
      {"name": "Toasted Sesame Seeds", "quantity_used": 10, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Smoothie Bowl",
    "description": "1. Place frozen mixed berries and frozen banana in a blender.\n2. Add Greek yogurt and almond milk.\n3. Blend on high power until completely smooth and very thick — the mixture should hold toppings without sinking. Add more almond milk a tablespoon at a time only if needed.\n4. Pour the thick smoothie into a bowl and spread evenly with a spoon.\n5. Arrange granola along one edge of the bowl.\n6. Top with fresh berries, scatter chia seeds, and add coconut flakes.\n7. Drizzle honey over the entire bowl.\n8. Serve immediately while the base is still frozen and thick.",
    "category": "fit",
    "yield_amount": 1,
    "yield_unit": "bowl",
    "image_url": "https://www.themealdb.com/images/media/meals/rpvptu1511641092.jpg",
    "ingredients": [
      {"name": "Frozen Mixed Berries", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Frozen Banana", "quantity_used": 120, "unit_of_measure": "g"},
      {"name": "Greek Yogurt", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Almond Milk", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Granola", "quantity_used": 60, "unit_of_measure": "g"},
      {"name": "Fresh Berries", "quantity_used": 80, "unit_of_measure": "g"},
      {"name": "Honey", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Chia Seeds", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Coconut Flakes", "quantity_used": 10, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Vegetable Soup",
    "description": "1. Dice onion, carrot, celery, and sweet potato into 1.5cm pieces. Mince garlic.\n2. Heat olive oil in a large pot over medium heat. Add onion, carrot, and celery; cook for 6–7 minutes until softened.\n3. Add garlic, dried oregano, bay leaves, and red pepper flakes; cook for 1 minute.\n4. Add sweet potato and stir to combine.\n5. Pour in vegetable broth and canned diced tomatoes. Season with salt. Bring to a boil.\n6. Reduce heat and simmer covered for 20 minutes until all vegetables are completely tender.\n7. Remove bay leaves. Taste and adjust seasoning.\n8. Serve hot with a drizzle of olive oil and crusty bread on the side.",
    "category": "fit",
    "yield_amount": 6,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/x2fw9e1560460636.jpg",
    "ingredients": [
      {"name": "Extra Virgin Olive Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Onion", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Carrot", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Celery", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Sweet Potato", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Vegetable Broth", "quantity_used": 1500, "unit_of_measure": "ml"},
      {"name": "Canned Diced Tomatoes", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Dried Oregano", "quantity_used": 3, "unit_of_measure": "g"},
      {"name": "Bay Leaves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Red Pepper Flakes", "quantity_used": 1, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Chocolate Chip Cookies",
    "description": "1. Melt butter in a saucepan over medium heat and continue cooking, swirling frequently, until it turns golden brown and smells nutty. Pour into a large bowl and cool for 5 minutes.\n2. Whisk both sugars into the browned butter until smooth. Whisk in eggs one at a time, then add vanilla extract.\n3. Sift in flour, baking soda, and salt. Fold with a spatula until just combined.\n4. Fold in chocolate chips. Cover and refrigerate the dough for at least 1 hour (overnight preferred for deeper flavour).\n5. Preheat oven to 180°C / 350°F and line baking trays with parchment paper.\n6. Roll dough into balls of about 40g each and place 5cm apart on the trays.\n7. Bake for 10–12 minutes until the edges are set but the centers look underdone.\n8. Cool on the tray for 5 minutes before transferring to a wire rack — they firm up as they cool.",
    "category": "snack",
    "yield_amount": 24,
    "yield_unit": "cookies",
    "image_url": "https://www.themealdb.com/images/media/meals/sktequ1764447186.jpg",
    "ingredients": [
      {"name": "All-Purpose Flour", "quantity_used": 280, "unit_of_measure": "g"},
      {"name": "Unsalted Butter", "quantity_used": 170, "unit_of_measure": "g"},
      {"name": "Granulated Sugar", "quantity_used": 113, "unit_of_measure": "g"},
      {"name": "Brown Sugar", "quantity_used": 220, "unit_of_measure": "g"},
      {"name": "Large Eggs", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Vanilla Extract", "quantity_used": 10, "unit_of_measure": "ml"},
      {"name": "Baking Soda", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Chocolate Chips", "quantity_used": 340, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Brownies",
    "description": "1. Preheat oven to 175°C / 350°F. Grease a 20x20cm baking pan and line with parchment paper.\n2. Melt butter in a saucepan over medium heat. Remove from heat and whisk in vegetable oil and cocoa powder until smooth.\n3. Whisk in sugar until fully combined. Add eggs one at a time, whisking vigorously after each. Add vanilla extract.\n4. Sift in flour and salt. Fold gently with a spatula until just combined — do not over-mix.\n5. Fold in chocolate chips.\n6. Pour batter into the prepared pan and spread evenly.\n7. Bake for 20–25 minutes until a toothpick inserted in the center comes out with moist crumbs — not wet batter, not dry.\n8. Cool completely in the pan before slicing into 16 pieces.",
    "category": "snack",
    "yield_amount": 16,
    "yield_unit": "pieces",
    "image_url": "https://www.themealdb.com/images/media/meals/yypvst1511386427.jpg",
    "ingredients": [
      {"name": "Unsalted Butter", "quantity_used": 112, "unit_of_measure": "g"},
      {"name": "Vegetable Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Unsweetened Cocoa Powder", "quantity_used": 60, "unit_of_measure": "g"},
      {"name": "All-Purpose Flour", "quantity_used": 83, "unit_of_measure": "g"},
      {"name": "Granulated Sugar", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Large Eggs", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Vanilla Extract", "quantity_used": 5, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Chocolate Chips", "quantity_used": 100, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Banana Bread",
    "description": "1. Preheat oven to 175°C / 350°F. Grease a 23x13cm loaf tin.\n2. Peel and mash very ripe bananas in a large bowl until smooth.\n3. Melt butter and whisk into the bananas. Add sugar and whisk until combined.\n4. Beat in eggs one at a time, then add vanilla extract.\n5. In a separate bowl, whisk together flour, baking powder, ground cinnamon, and salt.\n6. Fold the dry ingredients into the wet mixture until just combined — a few lumps are fine.\n7. Pour batter into the prepared loaf tin and smooth the top.\n8. Bake for 55–65 minutes until a toothpick inserted in the center comes out clean. If the top browns too quickly, cover loosely with foil for the last 15 minutes.\n9. Cool in the tin for 10 minutes, then turn out onto a wire rack.",
    "category": "snack",
    "yield_amount": 1,
    "yield_unit": "loaf",
    "image_url": "https://www.themealdb.com/images/media/meals/sywswr1511383814.jpg",
    "ingredients": [
      {"name": "Ripe Bananas", "quantity_used": 345, "unit_of_measure": "g"},
      {"name": "Unsalted Butter", "quantity_used": 115, "unit_of_measure": "g"},
      {"name": "Granulated Sugar", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Large Eggs", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "All-Purpose Flour", "quantity_used": 270, "unit_of_measure": "g"},
      {"name": "Baking Powder", "quantity_used": 7.5, "unit_of_measure": "g"},
      {"name": "Ground Cinnamon", "quantity_used": 5, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Vanilla Extract", "quantity_used": 5, "unit_of_measure": "ml"}
    ]
  },
  {
    "name": "Energy Balls",
    "description": "1. Add peanut butter and honey to a large bowl and mix until smooth.\n2. Stir in vanilla extract.\n3. Add old fashioned oats and mix until evenly coated with the peanut butter mixture.\n4. Stir in chia seeds, chocolate chips, and salt. Mix until well distributed.\n5. Cover and refrigerate the mixture for 30 minutes — it needs to firm up to be rollable.\n6. Remove from fridge and use a tablespoon to scoop out portions. Roll each between your palms to form a smooth ball.\n7. Place on a parchment-lined tray and refrigerate for at least 15 minutes before serving.\n8. Store in an airtight container in the fridge for up to 1 week.",
    "category": "snack",
    "yield_amount": 20,
    "yield_unit": "balls",
    "image_url": "https://www.themealdb.com/images/media/meals/1544384070.jpg",
    "ingredients": [
      {"name": "Peanut Butter", "quantity_used": 120, "unit_of_measure": "g"},
      {"name": "Old Fashioned Oats", "quantity_used": 90, "unit_of_measure": "g"},
      {"name": "Honey", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Chia Seeds", "quantity_used": 10, "unit_of_measure": "g"},
      {"name": "Chocolate Chips", "quantity_used": 60, "unit_of_measure": "g"},
      {"name": "Vanilla Extract", "quantity_used": 5, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Hummus",
    "description": "1. Drain and rinse the canned chickpeas. Reserve a few whole chickpeas for garnish if desired.\n2. Add tahini and lemon juice to a food processor and blend for 1 minute until creamy and pale. Scrape down the sides.\n3. Add minced garlic, ground cumin, and salt. Blend for another 30 seconds.\n4. Add the chickpeas and blend for 1 minute, scraping down the sides as needed.\n5. With the processor running, drizzle in cold water gradually until the hummus reaches a smooth, creamy, light consistency — about 1–2 minutes of blending total.\n6. Taste and adjust lemon juice, garlic, and salt.\n7. Spoon into a bowl and use the back of a spoon to create a swirl on top. Drizzle generously with olive oil.\n8. Serve with warm pita, fresh vegetables, or use as a spread.",
    "category": "snack",
    "yield_amount": 500,
    "yield_unit": "g",
    "image_url": "https://www.themealdb.com/images/media/meals/gpon5u1763801180.jpg",
    "ingredients": [
      {"name": "Canned Chickpeas", "quantity_used": 400, "unit_of_measure": "g"},
      {"name": "Tahini", "quantity_used": 120, "unit_of_measure": "g"},
      {"name": "Lemon Juice", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Garlic Cloves", "quantity_used": 2, "unit_of_measure": "unit"},
      {"name": "Extra Virgin Olive Oil", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Cold Water", "quantity_used": 80, "unit_of_measure": "ml"},
      {"name": "Ground Cumin", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Guacamole",
    "description": "1. Halve and pit the avocados. Scoop the flesh into a bowl and drizzle lime juice over it immediately to prevent browning.\n2. Finely dice red onion, roma tomato, and jalapeño (remove seeds for less heat). Chop fresh cilantro. Mince garlic.\n3. Using a fork, mash the avocado to your preferred consistency — slightly chunky gives the best texture.\n4. Fold in diced onion, tomato, jalapeño, cilantro, and minced garlic.\n5. Stir in ground cumin and salt. Mix gently to combine.\n6. Taste and adjust lime juice, salt, and jalapeño heat.\n7. Serve immediately with tortilla chips.\n8. To store, press plastic wrap directly onto the surface and refrigerate for up to 2 hours.",
    "category": "snack",
    "yield_amount": 350,
    "yield_unit": "g",
    "image_url": "https://www.themealdb.com/images/media/meals/flrajf1762341295.jpg",
    "ingredients": [
      {"name": "Ripe Avocados", "quantity_used": 3, "unit_of_measure": "unit"},
      {"name": "Lime Juice", "quantity_used": 30, "unit_of_measure": "ml"},
      {"name": "Red Onion", "quantity_used": 40, "unit_of_measure": "g"},
      {"name": "Roma Tomato", "quantity_used": 100, "unit_of_measure": "g"},
      {"name": "Fresh Cilantro", "quantity_used": 20, "unit_of_measure": "g"},
      {"name": "Jalapeño Pepper", "quantity_used": 20, "unit_of_measure": "g"},
      {"name": "Garlic Cloves", "quantity_used": 1, "unit_of_measure": "unit"},
      {"name": "Ground Cumin", "quantity_used": 2.5, "unit_of_measure": "g"},
      {"name": "Salt", "quantity_used": 2.5, "unit_of_measure": "g"}
    ]
  },
  {
    "name": "Tiramisu",
    "description": "1. Brew strong espresso and let it cool to room temperature. Stir in dark rum.\n2. Separate eggs. In a large bowl, beat egg yolks and sugar together until the mixture turns pale and thick, about 3–4 minutes.\n3. Add mascarpone to the egg yolk mixture and beat until smooth and creamy.\n4. In a separate clean bowl, beat egg whites with a pinch of salt to stiff peaks.\n5. Using a spatula, gently fold the egg whites into the mascarpone cream in thirds, keeping as much air as possible.\n6. Working quickly, dip each ladyfinger into the espresso mixture for 2–3 seconds — do not soak or they will become soggy.\n7. Arrange a layer of dipped ladyfingers in the bottom of a 23x30cm dish. Spread half the mascarpone cream evenly on top. Repeat with a second layer of ladyfingers and the remaining cream.\n8. Cover and refrigerate for at least 6 hours, preferably overnight. Dust generously with unsweetened cocoa powder just before serving.",
    "category": "snack",
    "yield_amount": 8,
    "yield_unit": "portions",
    "image_url": "https://www.themealdb.com/images/media/meals/yypvst1511386427.jpg",
    "ingredients": [
      {"name": "Strong Espresso", "quantity_used": 360, "unit_of_measure": "ml"},
      {"name": "Large Eggs", "quantity_used": 4, "unit_of_measure": "unit"},
      {"name": "Granulated Sugar", "quantity_used": 150, "unit_of_measure": "g"},
      {"name": "Mascarpone Cheese", "quantity_used": 450, "unit_of_measure": "g"},
      {"name": "Ladyfinger Cookies", "quantity_used": 200, "unit_of_measure": "g"},
      {"name": "Unsweetened Cocoa Powder", "quantity_used": 20, "unit_of_measure": "g"},
      {"name": "Dark Rum", "quantity_used": 60, "unit_of_measure": "ml"},
      {"name": "Salt", "quantity_used": 1, "unit_of_measure": "g"}
    ]
  }
]
RECIPES_EOF

jq -c '.[]' "$tmpfile" | while IFS= read -r recipe; do
  name=$(printf '%s' "$recipe" | jq -r '.name')
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$BASE_URL/recipes" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$recipe")
  printf '%s %s\n' "$code" "$name"
done
