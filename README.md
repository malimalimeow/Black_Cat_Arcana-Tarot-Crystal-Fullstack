# Black CAT ARCANA

#### Video Demo: https://youtu.be/XqFgSrxDcdk

### Description
Black CAT ARCANA is a web application that combines tarot reading and crystal information.

Tarot reading is often used to reflect on possible futures. The result is not fixed, and it depends on how people face their situation. Crystals are also commonly associated with ideas such as luck, love, and emotional support.  
Because I run a small crystal-related business, I wanted to combine these two concepts into one project.

The website uses a dark and mysterious style, with a black cat theme, while keeping the interface simple and friendly.

### Project Structure
This project is divided into three main parts:

1. **Flask** – Handles the logic, loads JSON files, and updates SQL.
2. **HTML, CSS, JavaScript** – Controls the visual presentation and interactions.
3. **SQL** – Stores all data used by the website.

#### Main Features
1. **Tarot**
   - Tarot cards are generated using Python’s random module and a JSON file.
   - The JSON file contains tarot meanings and related crystal suggestions.
   - JSON is used because the tarot deck has a fixed number of 78 cards and is easy to update.
   - Users can draw one tarot card every 24 hours to keep the reading meaningful.
   - If a user cannot draw a new card, they can still view their previous result.

2. **Crystal**
   - Displays a list of crystals and individual crystal detail pages.
   - All crystal pages use the same HTML template.
   - Crystal data is stored in SQL, making it easy to add new crystals in the future.
   - The system allows adding new data while preventing accidental changes to existing records.

3. **Login, Registration, Reset Password, Favourite**
   - All pages except the crystal showcase require login.
   - After logging in, the system records: login time, tarot draws, favourite crystals, chosen tarot category. These records are used later for dashboard analysis.
   - The favourite button is a toggle heart on each crystal image. It updates instantly without refreshing the page, and the final status is saved when the user leaves the page.

4. **Dashboard**
   - The dashboard is separated into two pages: User Activity and Content. Both pages require direct URL access and admin login, providing double security.
   - **User Activity**: shows daily login data (“daily views”), daily tarot draws, and weekly most active users. Helps analyze user behavior.
   - **Content**: shows weekly top-favourited crystals, favourite rate of each crystal, and crystal category choices. Helps understand user preferences and plan future content or events.

### Design Choices and Trade-offs
I started the course quite late and had limited time for development. Because of this:
- Only one tarot card and three categories are fully implemented.
- Only ten crystals are included.  

However, this is enough to demonstrate the full idea and system design.

### Potential Improvements and Enhancements
- Add more tarot cards and allow multi-card spreads.
- Improve animations to make the website more responsive.
- Expand the crystal database.

### Crystal + Favourite Feature
This feature helps with future business and event planning. On this website, the favourite button is a heart-shaped toggle, but in a real commercial website, it could act like a shopping cart to record customers' preferred items.  
Using this data, I can recommend similar products to customers based on their favourites, improving sales and customer satisfaction.

### Dashboard Applications
For example, if some crystals are found to be very popular, I can use the data to:
- Analyze the characteristics of high like-rate crystals, such as their color, energy, or type.
- Add similar products to the shop list based on the analysis, enhancing product offerings.
- Understand customer preferences to plan future events, promotions, or themed packages.
- By collecting daily login counts and tarot draw counts, I can see whether most users visit mainly to draw tarot cards, which helps evaluate the attractiveness of this activity.  
- I also track which crystal category users view after drawing a tarot card, helping me understand the purpose behind their tarot draws and allowing me to plan special events focused on those specific crystal categories.

### Reflection / Learning Outcome
- **Flask + SQL**: At first, I was not familiar with SQL and often quoted data incorrectly. After some practice, I was able to retrieve the correct data.  
- **Frontend Skills**: I learned more about CSS, HTML, and Chart.js applications.  
- **Problem Solving**: Some ideas were unclear initially, so I asked AI for methods and then applied them myself in the web app. Although the process was sometimes messy, I can refine it later.

### Conclusion
Black CAT ARCANA combines tarot reading, crystal energy, and user analytics into a themed, interactive web experience.  
Even though the dataset is small due to time constraints, the system is functional, extendable, and clearly shows the intended conc