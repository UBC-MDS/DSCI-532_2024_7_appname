**Milestone 3 Reflection**

Milestone 3 featured a complete overhaul to the interface of our dashboard.

Adhering to our minimal viable product (MVP) design strategy, we presented our dashboard to our visual design expert Dr. Joel Ostblom. He offered numerous helpful suggestions and tips for improvement.
Joel observed that most of our widgets contained similar information and were controlled by the same global filters.
Thus, recognizing the need for a more varied presentation of data, we unanimously chose to start afresh with our interface design.

This re-design involved scrapping the global drop-down menu filters in place of local filters, tailored to each widget.
Apart from a single global filter for continent, each widget is now displayed in its own 'card' and is self-contained. This allows the user to get a holistic view of what types of information the dashboard can display, then afterwards, focus on the widget that piques their curiosity. A zoom in/zoom out approach to design.
Our previous design required the user to frequently alternate attention between the global filters and the local widgets.

Following the reduction of global filters, we broadened our dashboard's functionality by introducing new widgets.

These additions include:

- An interactive Heatmap of the world showing the relationship between country and salary.
- A density distribution of salary across all data scientists.
- A bar chart that sorts the average salary by data science specialty type (e.g. Data Architect vs Financial Data Analyst).
- A box plot that shows the relationship between work arrangement (e.g. Remote vs Local) and salary. 
- A box plot that shows the relationship between work experience and salary.

**Addressing Feedback**

Here is a checklist of the improvements made and the source of the feedback that motivated the improvement.

Joel:

- Three charts showing salary, but all are different viz choices. Make viz choices consistent for same value. (complete)
- Redesign layouts as per new sketch (complete)
- Pick continent based on location. Zoom (complete)
- Add map, choropleth based on salary (complete)
- One card each for the boxplots (complete)

Internal & Peers:

- Wrangle the data to display labels that are interpretable to a general audience. (complete)
- Remove the option to filter for insufficient data (complete)
- Improve color scheme to adhere to DSCI 531 principles of good design (complete)

**Future Improvements**

We intend to release our latest prototype to get more feedback before the final polished release in milestone 4.

"Select countries from map, update all charts" was a suggestion by Joel we chose to partially implement for this milestone.
The trade-off for this suggestion was that most countries do not have sufficient data to present meaningful graphs.
Our solution to this trade-off was to allow the option to filter by continent instead of country. 

However, next milestone we might implement a more complex filtering system to allow users to filter between countries with sufficient data within the same continent.

We intend to make our widgets more interactive and will brainstorm strategies on how to best accomplish that.
Cosmetically, there is room for polish on the aesthetics of our dashboard. The color scheme is somewhat basic and uniform.

We eagerly anticipate further feedback to refine our dashboard, with a commitment to the principles of iterative design.
