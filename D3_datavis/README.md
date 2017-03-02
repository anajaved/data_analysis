Summary - briefly introduce your data visualization and add any context that can help readers understand it

The visualization focuses on the passengers of the Titanic tragedy and explores information regarding their backgrounds, and whether they survived or not. The graph allows you to explore survivors's gender, age, socioeconomic class, and place of living before the trip. Viewers can click on the buttons to examine the different variables and hover over the bars to see exact values.

A common finding that can be obtained from interacting with the data is far more lower class men died as the Titanic sank. 


Design - explain any design choices you made including changes to the visualization after collecting feedback

I utilized Dimple.js and D3.js to create the graph, and wanted the viewer to explore all facets of the data as possible so I incorporated interactivity with the help of the buttons. Initially my graph only examined the backgrounds of passengers who survived, however upon exploring the feedback I received from my peers, I realized having both passenger outcomes (survived and dead) on the graph was important for context. I achieved this by implementing a double bar graph. 

I also ensured to only display certain colors pertaining to the graph in the legend. Initially all the legend colors were on display as the user jumped between graphs, however I acknowledged that this can be confusing and made the appropriate changes. 

Finally, I changed the opacity of the bars to prevent any confusion on where the lines began and ended. 


Feedback - include all feedback you received from others on your visualization 

 >> first visualization: http://bl.ocks.org/anajaved/raw/5f91e831c60043108ace189dfe861daf/ 
 
 First feedback: "The message conveyed is very clear, it shows very well the distribution of the survived people from the disaster, with nice designed interaction buttons. When you click the button, the previous 'rect' will still be there, though it's very light with color. Is it possible to fix that code?"

 >> second visualization: http://bl.ocks.org/anajaved/raw/fa8fcde396d93c12b94bea817fe6d242/

 Second feedback: "I enjoyed the visualization. It allows the viewer to explore the key relationships in a clear fashion. A minor improvement could be to change the legend for each button press to make it easier to match the categories with the colors."

 Third feedback: "I guess what jumps out and what might be the key takeaway of this visualisation, is that by gender, location, or age group, more survivors were first class passengers than belonged to either second or third class. Perhaps I would consider experimenting with the y axis a bit here. I think rather than absolute number of survivors it showed share of survivors in a class, the pattern of survival as affected by class would be clearer."

 >> final visualization: http://bl.ocks.org/anajaved/raw/09f12e8919612d1e3570a3b89065db61/

 
Resources - list any sources you consulted to create your visualization
•	https://www.kaggle.com/c/titanic-gettingStarted/data 
•	http://dimplejs.org/examples_index.html
•	https://www.w3schools.com/jsref/jsref_continue.asp 
