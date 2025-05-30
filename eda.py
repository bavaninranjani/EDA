# -*- coding: utf-8 -*-
"""
"""

import pandas as pd              # For data manipulation and DataFrame handling
import numpy as np               # For numerical operations and array handling
import seaborn as sns            # For statistical data visualization (heatmaps, boxplots, etc.)
import matplotlib.pyplot as plt  # For plotting graphs (line, bar, scatter, etc.)

haberman = pd.read_csv("haberman.csv",header=None,names=['age','year','axil_nodes','survival_status'])

print(haberman.shape)
# Output: (306, 4) → 306 records, 4 features

list(haberman['survival_status'].unique())
# Unique Survival status 1=Survived 2=Non Survived

haberman.describe() # Descriptive Statitics

haberman.info() # Concise Summary
# Data Set doesn't have any null values

"""# Objective:
Find the data points of features which would help in classifying survival_status.
"""

haberman['survival_status'].value_counts()

"""# Observation
There are 225 data points of patients who survived with in 5 yrs and 81 data points who didn't survive
"""

sns.FacetGrid(haberman, hue="survival_status", height=6) \
   .map(plt.scatter, "age", "axil_nodes") \
   .add_legend();
plt.title('axil Nodes vs Age of patients')
plt.show();

"""# Observation
1.Patients with fewer than 5 axillary nodes (i.e., axil_nodes < 5) were more likely to survive beyond 5 years after surgery, as indicated by the clustering of survivors in this region.

2.No strong patterns were observed with respect to other features like age or year of operation; the data appears scattered and overlapping across survival classes, making classification based on those features less effective.

# 2 D Scatter Plot
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Close any previous plots
plt.close()

# Set aesthetic style
sns.set_style("whitegrid")

# Generate pairwise scatter plots for selected features
sns.pairplot(
    haberman,
    hue="survival_status",            # Color by survival status
    vars=['age', 'year', 'axil_nodes'],  # Variables to include in the plot
    height=3                          # Size of each subplot
)

plt.show()

"""# Observation
1.All possible pairwise combinations among age, year, and axil_nodes have been visualized using scatter plots and histograms.

2.Blue points represent patients who survived 5 years or longer after surgery (survival_status = 1).

3.Orange points represent patients who did not survive beyond 5 years (survival_status = 2).

4.Among the features analyzed, age and axil_nodes show relatively better separation between the two survival classes and appear to be more useful in predicting survival outcomes.
"""

survived_5_yrs = haberman[haberman["survival_status"] == 1] # Patients who survived 5 years or more
dead = haberman[haberman["survival_status"] == 2]

#Patients who died within 5 years
print(survived_5_yrs["age"].describe())

"""#Interpretation:
1.Mean age of survivors: ~52 years

2.Youngest survivor: 30 years old

3.Oldest survivor: 77 years old

4.Age Range 30 to 77
"""

print(dead["age"].describe())

"""# Interpretation
1.Mean age : ~53 years

2.Youngest non-survivor : 33 years old

3.Oldest non-survivor: 83 years old

4.Age Range 34 to 83

"""

print(survived_5_yrs["axil_nodes"].describe())
#summary statistics for the number of positive axillary lymph nodes among patients who survived 5 years or more.

"""# Interpretation
1.Median (50%) = 0 → More than half of survivors had no positive lymph nodes.

2.Mean = 2.79, but note the standard deviation is high (~5.87) → skewed distribution.

3.75% of survivors had 3 or fewer positive nodes.

4.Outliers exist (e.g., someone with 52 nodes still survived).

"""

print(dead["axil_nodes"].describe())
# summary statistics for the number of positive axillary lymph nodes in patients who did not survive beyond 5 years.

"""# Observations
1.Deceased patients have higher node counts on average, and a wider spread of values.

2.Median node count is 4x higher in the deceased group.

3.axil_nodes is the strongest feature for classifying survival.

# Histograms
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Set seaborn style
sns.set_style("whitegrid")
plt.close()

# Create histogram with kernel density estimate by survival status
sns.FacetGrid(haberman, hue="survival_status", height=5) \
   .map(sns.histplot, "age", kde=True, stat="density", bins=15, alpha=0.6) \
   .add_legend()

plt.title('Age Distribution by Survival Status')
plt.xlabel('Age')
plt.ylabel('Density')
plt.show()

"""# Interpretation

1.Lot of overlap, meaning age alone is not a strong predictor of survival.

2.Most patients, regardless of survival status, are in their 40s to 60s.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Close previous plots and set style
plt.close()
sns.set_style("whitegrid")

# Plot year distribution by survival status
sns.FacetGrid(haberman, hue="survival_status", height=5) \
   .map(sns.histplot, "year", kde=True, stat="density", bins=10, alpha=0.6) \
   .add_legend()

plt.title('Year of Operation Distribution by Survival Status')
plt.xlabel('Year of Operation')
plt.ylabel('Density')
plt.show()

"""# Interpretation
1.There is no strong class separation based on year of operation alone.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and close previous plots
plt.close()
sns.set_style("whitegrid")

# Plot the distribution of axillary nodes by survival status
sns.FacetGrid(haberman, hue="survival_status", height=5) \
   .map(sns.histplot, "axil_nodes", kde=True, stat="density", bins=20, alpha=0.6) \
   .add_legend()

plt.title('Axillary Nodes Distribution by Survival Status')
plt.xlabel('Number of Positive Axillary Nodes')
plt.ylabel('Density')
plt.show()

"""# Observation
1.Survivors (status = 1) are heavily concentrated at axil_nodes = 0.


2.Non-survivors (status = 2) have a broader, right-skewed distribution with higher node counts.

# PDF and CDFs Plots
"""

import numpy as np
import matplotlib.pyplot as plt

# PDF and CDF for survivors
counts, bin_edges = np.histogram(survived_5_yrs['age'], bins=10, density=True)
pdf = counts / sum(counts)
cdf = np.cumsum(pdf)

# Plot for survivors
plt.plot(bin_edges[1:], pdf, label='PDF of Survived', color='blue')
plt.plot(bin_edges[1:], cdf, label='CDF of Survived', linestyle='--', color='blue')

# PDF and CDF for deceased
counts, bin_edges = np.histogram(dead['age'], bins=10, density=True)
pdf = counts / sum(counts)
cdf = np.cumsum(pdf)

# Plot for deceased
plt.plot(bin_edges[1:], pdf, label='PDF of Deceased', color='orange')
plt.plot(bin_edges[1:], cdf, label='CDF of Deceased', linestyle='--', color='orange')

# Final plot formatting
plt.title('PDF and CDF of Age by Survival Status')
plt.xlabel('Age')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)
plt.show()

counts, bin_edges = np.histogram(survived_5_yrs['axil_nodes'], bins=10,
                                 density = True)
pdf = counts/(sum(counts))
print(pdf);
print(bin_edges);
cdf = np.cumsum(pdf)
plt.plot(bin_edges[1:],pdf);
plt.plot(bin_edges[1:], cdf)

counts, bin_edges = np.histogram(dead['axil_nodes'], bins=10,
                                 density = True)
pdf = counts/(sum(counts))
print(pdf);
print(bin_edges);
cdf = np.cumsum(pdf)
plt.plot(bin_edges[1:],pdf);
plt.plot(bin_edges[1:], cdf)
plt.title('Axil_Nodes PDF and CDF')

plt.gca().legend(('PDF of survived','CDF of survived ', 'PDF of dead ', 'CDF of dead'))



plt.show();

"""# Observation

1.Survivors and non-survivors will have similar age distributions with slight shifts, often overlapping.

2.This visualization reinforces that age alone is not highly discriminatory.

"""

import numpy as np
import matplotlib.pyplot as plt

# PDF and CDF for patients who survived 5+ years
counts, bin_edges = np.histogram(survived_5_yrs['year'], bins=10, density=True)
pdf = counts / sum(counts)
cdf = np.cumsum(pdf)

plt.plot(bin_edges[1:], pdf, label='PDF of Survived', color='blue')
plt.plot(bin_edges[1:], cdf, label='CDF of Survived', linestyle='--', color='blue')

# PDF and CDF for patients who died within 5 years
counts, bin_edges = np.histogram(dead['year'], bins=10, density=True)
pdf = counts / sum(counts)
cdf = np.cumsum(pdf)

plt.plot(bin_edges[1:], pdf, label='PDF of Deceased', color='orange')
plt.plot(bin_edges[1:], cdf, label='CDF of Deceased', linestyle='--', color='orange')

# Final plot formatting
plt.title('PDF and CDF of Year of Operation by Survival Status')
plt.xlabel('Year of Operation')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)
plt.show()

"""# Observation

1.Expect significant overlap in year distributions for both classes.

2.Any minor skew may reflect treatment advances or dataset bias, but year is not a strong predictor of survival outcome based on PDF/CDF shape alone.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Create the boxplot
sns.boxplot(x='survival_status', y='age', data=haberman)

# Add title and axis labels
plt.title('Age Distribution by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Age')
plt.grid(True)
plt.show()

"""# Interpretation

1.Median ages of survivors and non-survivors are very close.

2.Interquartile ranges (IQRs) overlap significantly.

3.There may be more outliers among older non-survivors, but overall, age doesn’t offer strong class separation.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Boxplot of axillary node counts by survival status
sns.boxplot(x='survival_status', y='axil_nodes', data=haberman)

# Add title and labels
plt.title('Axillary Nodes by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Number of Positive Axillary Nodes')
plt.grid(True)
plt.show()

"""# Interpretation

1.Survivors (status = 1):

-->Median number of nodes is 0.

-->Very low IQR — majority have 0 to 3 nodes.

-->Many values are zero, indicating no spread in most patients.

2.Non-survivors (status = 2):

-->Higher median (~4).

-->Wider IQR and presence of higher outliers (up to 50+).

-->More variability in node counts, indicating a higher burden of disease.


"""

import seaborn as sns
import matplotlib.pyplot as plt

# Boxplot of year of operation grouped by survival status
sns.boxplot(x='survival_status', y='year', data=haberman)

# Add labels and title
plt.title('Year of Operation by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Year of Operation (19xx)')
plt.grid(True)
plt.show()

"""# Interpretation

1.Median and IQR (Interquartile Range) for both groups are very close, typically between 1958 and 1969.

2.There’s no significant trend suggesting patients operated on in a specific year had better survival outcomes.
"""

# Violin plot showing age distribution by survival status
sns.violinplot(x="survival_status", y="age", data=haberman, inner="box", height=6)

# Add title and labels
plt.title('Age Distribution by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Age')
plt.grid(True)
plt.show()

"""# Interpretation

1.The distributions for both classes are quite similar, with peaks around 45–60 years.

2.No significant multimodal distribution, and considerable overlap between the two survival groups.

3.Reinforces that age alone is not a strong predictor of survival.

"""

sns.violinplot(x="survival_status", y="age", data=haberman, inner="box", height=6)

# Add title and labels
plt.title('Age Distribution by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Age')
plt.grid(True)
plt.show()

"""# Interpretation

1.The distributions for both classes are quite similar, with peaks around 45–60 years.

2.No significant multimodal distribution, and considerable overlap between the two survival groups.

3.Reinforces that age alone is not a strong predictor of survival.
"""

plt.figure(figsize=(8, 6))

# Violin plot of axillary nodes count by survival status
sns.violinplot(x="survival_status", y="axil_nodes", data=haberman, inner="box")

# Add title and labels
plt.title('Axillary Nodes by Survival Status')
plt.xlabel('Survival Status (1 = Survived ≥5 yrs, 2 = Died <5 yrs)')
plt.ylabel('Number of Positive Axillary Nodes')
plt.grid(True)
plt.show()

"""# Interpretation

1.Survivors (survival_status = 1):

-->Distribution is tightly concentrated near 0.

-->Long, thin tail — very few had high node counts.

2.Non-survivors (survival_status = 2):

-->Distribution is broader and shifted right.

-->Indicates more positive lymph nodes, with a higher spread and mean.
"""

# Create joint KDE plot of age vs year
g = sns.jointplot(
    x='age',
    y='year',
    kind='kde',
    data=haberman,
    fill=True,
    cmap='Blues',
    height=6
)

# Set plot title correctly using the jointplot object
g.fig.suptitle('Age vs Year - KDE Contour Plot', fontsize=14)
g.fig.tight_layout()
g.fig.subplots_adjust(top=0.93)  # Adjust to fit title
plt.show()

"""# Interpretation

1.Contour rings show regions of high data concentration.

2.This plot will likely show no strong correlation between age and year, meaning:

-->lder and younger patients were operated on throughout all years in the dataset.

-->Age and year of operation are likely independent features in this dataset.

# Insights from Box Plots and Violin Plots

1.Axillary Nodes (axil_nodes):
 -->Both box plots and violin plots indicate that most survivors had fewer than 3 positive axillary lymph nodes.
-->There are a few outliers with high node counts among survivors, but these are rare.
-->This confirms that low axillary node count is a strong indicator of long-term survival.
2.Year of Operation (year):
-->The plots suggest that a higher number of non-survivors underwent surgery between the years 1959 and 1963 compared to 1964 to 1969.
-->This could point to advancements in treatment or surgical procedures post-1963, though this is speculative without clinical context.

3.Age vs Year Relationship:
-->A significant concentration of surgeries occurred between 1959 and 1963 for patients in the age group 42 to 58.
-->This highlights a demographic cluster that may warrant further analysis in conjunction with survival outcomes.

# Final Thoughts
1.Class Imbalance
The dataset is imbalanced, with significantly more data points for survivors compared to non-survivors. To ensure robust model performance, especially for the minority class, techniques such as oversampling, undersampling  may be required.

2.Feature Importance
Among all features, axil_nodes (number of positive axillary lymph nodes) is the most informative predictor of survival. Models should account for this, potentially assigning it greater weight or feature importance in feature selection and interpretation.

3.Complex Decision Boundary
The relationship between input features and survival status is not linearly separable. Therefore, applying a simple rule-based (if-then-else) logic is insufficient. More sophisticated classification models—such as logistic regression, decision trees, or ensemble methods—are needed to capture the non-linear patterns and interactions between features.
"""



















































