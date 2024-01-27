import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt


import scipy.stats as stats

df = pd.read_excel('Data.xlsx')

# Creating the box plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Keyboard_layout', y='WPM', hue='Typing_method', data=df)
plt.title('Box Plot of WPM for Different Typing Methods and Keyboard Layouts')
plt.xlabel('Keyboard Layout')
plt.ylabel('Words Per Minute (WPM)')
plt.show()

# Creating histogram
plt.figure(figsize=(12, 8))
sns.histplot(df['WPM'], bins=20, kde=True)
plt.title('Histogram of WPM')
plt.xlabel('Words Per Minute (WPM)')
plt.ylabel('Frequency')
plt.show()


# Check Homogeneity of variances
# Levene's test for equal variances
stat, p = stats.levene(df['WPM'][df['Keyboard_layout'] == 'ALPHABETICAL LAYOUT'], 
                       df['WPM'][df['Keyboard_layout'] == 'SPECIFIC LAYOUT'])
print('Levene\'s Test: Statistics=%.3f, p=%.3f' % (stat, p))

# Check Sphericity
mauchly_test = pg.sphericity(df, dv='WPM', within=['Keyboard_layout', 'Typing_method'], subject='Subject')
print(mauchly_test)

# Peform the repeated measures ANOVA
anova = AnovaRM(df, 'WPM', 'Subject', within=['Keyboard_layout', 'Typing_method'])
res = anova.fit()

print(res)

# Compare 'WPM' means across different 'Typing_method' using Tukey's HSD test
tukey = pairwise_tukeyhsd(endog=df['WPM'],     # Data
                          groups=df['Typing_method'],   # Groups
                          alpha=0.05)          # Significance level

print(tukey)


# Perform the post-hoc test to test interaction effect
posthoc = pg.pairwise_ttests(data=df, dv='WPM', between=['Keyboard_layout', 'Typing_method'], interaction=True, padjust='bonferroni')
posthoc.to_excel('posthoc_output.xlsx', index=False)