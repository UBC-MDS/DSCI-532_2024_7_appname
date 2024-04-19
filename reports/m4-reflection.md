**Milestone 4 Reflection**

After we completed Milestone 3, we showcased our latest design overhaul to our visual design expert, Dr. Joel Ostblom. This version introduced numerous enhancements, such as an interactive heat map visualizing average salaries by country and two new box-plots. Contrary to the lukewarm reception of our first release, Dr. Ostblom's response to these updates was overwhelmingly positive. His approval underscored our strategic pivot in design as a move in the right direction, validating the effectiveness of our new design.
Therefore, instead of doing a major functional overhaul like we did in our last update, this update focused on polished aesthetics and under-the-hood technical improvements to reduce latency.

**Addressing Feedback & Improvement List**

This section is a checklist of the additions and revisions of our latest version, primarily motivated by Joel's feedback found in this issue:
https://github.com/UBC-MDS/DSCI-532_2024_7_ds-compensation/issues/73

Improve Map Performance (complete) - We moved our dataframe and geojson to data.py so that they only get loaded once.
We shrunk the geojson file so that it only keeps the countries needed for the dataframe.

Add caching to improve performance (complete)

Change Histogram starting value on X axis from -500k to 0 (complete)

Improve y-axis histogram label (complete)

Change the color of the median salary to red to show that the dashed line is the median (complete)

Label the slider on the data salary job rankings bar chart (complete)

Bottom row widgets are misaligned, align them (complete)

Abbreviate very long names in the data e.g Data Scentist -> DS (complete)

Polish title appearance (complete)

**Future Improvements**

If we were to further improve our dashboard, we would look for another data science salary data set to increase the sample size of our data. The more data we have, the more we can allow our users to customize their research. We would add global filters so our users can execute precise queries and develop their own insights. Our current data size of ~600 samples restricts us to only offering broad overviews.
We would also fix the issue with our heatmap that allows the user to zoom out too far, effectivey showing multiple copies of the world side by side.

**Feedback for Joel**

Dr. Joel Ostblom has asked for our feedback in this document on his feedback and teachings.
We believe the lecture on improving performance (e.g caching) was particuarly useful. Prior to that lecture, little of the material in our MDS program had focused on run-time efficiency, but that skill is critical in many professional settings. We implemented caching in our latest milestone release and the improvements were immediatly noticed. We also found the weekly constructive criticsm of our dashboard by Joel useful. Having an experienced eye analyze the dashboard in its infancy allowed us to identify a major flaw in our design before we sunk too many resources into it.

If we had to change anything about the feedback we recieved, it would be on the timing of the peer feedback. Our peers reviewed an old model that had been totally re-designed by the time we recieved the feedback. If the deadline for feedback was moved up to Tuesday instead of Saturday, this problem would have been avoided.
