# %% [markdown]
# # PyCity Schools Analysis
# 
# - Your analysis here
#   
# ---

# %%
# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

# %% [markdown]
# ## District Summary

# %%
# Calculate the total number of unique schools
school_count = school_data_complete["school_name"].unique()
len(school_count)

# %%
# Calculate the total number of students
student_count = len(school_data_complete["Student ID"])
student_count

# %%
# Calculate the total budget
#total_budget = school_data["budget"].sum()
#OR
school_data_unique = school_data_complete.drop_duplicates(subset=['school_name'])
total_budget = school_data_unique["budget"].sum()

f"{total_budget:,d}"

# %%
# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].mean()
average_math_score

# %%
# Calculate the average (mean) reading score
average_reading_score = school_data_complete["reading_score"].mean()
print(average_reading_score)

# %%
# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage

# %%
# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage

# %%
# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate

# %%
# Create a high-level snapshot of the district's key metrics in a DataFrame (everything above)
data_dict = {'Total Schools':[school_count], 'Total Students':[student_count], 'Total Budget':[total_budget],'Average Math Score':[average_math_score],
             'Average Reading Score':[average_reading_score], 'Math Pass Rate':[passing_math_percentage], 'Reading Pass Rate':[passing_reading_percentage], 
             'Overall Pass Rate':[overall_passing_rate]}


district_summary = pd.DataFrame(data_dict)

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
#gives Total Budget Value $
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary["Average Math Score"] = district_summary["Average Math Score"].map("{:,.2f}".format)
district_summary["Average Reading Score"] = district_summary["Average Reading Score"].map("{:,.2f}".format)
district_summary["Math Pass Rate"] = district_summary["Math Pass Rate"].map("{:,.2f}%".format)
district_summary["Reading Pass Rate"] = district_summary["Reading Pass Rate"].map("{:,.2f}%".format)
district_summary["Overall Pass Rate"] = district_summary["Overall Pass Rate"].map("{:,.2f}%".format)

# Display the DataFrame
district_summary

# %% [markdown]
# ## School Summary

# %%
# Use the code provided to select all of the school types
school_NameTypes = school_data_complete[['school_name', 'type']].drop_duplicates(subset='school_name').sort_values('school_name')
school_names = list(school_NameTypes['school_name'])
school_types = list(school_NameTypes['type']) 
school_names


# %%
# Calculate the total student count per school
school_groups = school_data_complete.groupby(["type","school_name"])
per_school_countsdf = school_groups['Student ID'].count().reset_index().sort_values('school_name')
per_school_counts = list(per_school_countsdf['Student ID'])
per_school_counts

# %%
# Calculate the total school budget and per capita spending per school
per_school_budgetdf = school_groups['budget'].first().reset_index().sort_values('school_name')
per_school_budget = list(per_school_budgetdf['budget'])
per_school_capita = [i/o for i, o in zip(per_school_budget, per_school_counts)]
per_school_capita

# %%
# Calculate the average test scores per school
per_school_mathdf = school_groups['math_score'].mean().reset_index().sort_values('school_name')
per_school_readingdf = school_groups['reading_score'].mean().reset_index().sort_values('school_name')
per_school_reading = list(per_school_readingdf['reading_score'])
per_school_math = list(per_school_mathdf['math_score'])

# %%
# Calculate the number of students per school with math scores of 70 or higher
students_passing_mathgroup = school_data_complete[(school_data_complete["math_score"] >= 70)].groupby(['school_name'])
students_passing_math = list(students_passing_mathgroup['Student ID'].count())
school_students_passing_math = [(i/o) * 100 for i, o in zip(students_passing_math, per_school_counts)]
school_students_passing_math

# %%
,# Calculate the number of students per school with reading scores of 70 or higher
students_passing_readinggroup = school_data_complete[(school_data_complete["reading_score"] >= 70)].groupby(['school_name'])
students_passing_reading = list(students_passing_readinggroup['Student ID'].count())
school_students_passing_reading = [(i/o) * 100 for i, o in zip(students_passing_reading, per_school_counts)]
school_students_passing_reading

# %%
# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading_group = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
].groupby(["school_name"])
school_students_passing_math_and_reading = list(students_passing_math_and_reading_group['Student ID'].count())
school_students_passing_math_and_reading

# %%
# Use the provided code to calculate the passing rates
overall_passing_rate2 = [(i/o) * 100 for i, o in zip(school_students_passing_math_and_reading, per_school_counts)]
overall_passing_rate2

# %%
# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summarydict = {'School Name':school_names, 'School Type':school_types, 'Total Students':per_school_counts,'Total School Budget':per_school_budget,
             'Per Student Budget':per_school_capita, 'Average Math Score':per_school_math, 'Average Reading Score':per_school_reading, 
             '% Passing Math':school_students_passing_math, '% Passing Reading':school_students_passing_reading, '% Overall Passing':overall_passing_rate2}

#splitting per_school_summary into an unformatted version is to make Cell 26's code work better
#specifically, it keeps the dtype of Per Student Budget as float, which allows the binning process to work
per_school_summaryraw = pd.DataFrame(per_school_summarydict).set_index('School Name')
per_school_summaryraw.index.name = None
# Formatting
per_school_summary=per_school_summaryraw.copy()
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary

# %% [markdown]
# ## Highest-Performing Schools (by % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by='% Overall Passing', ascending = False)
top_schools.head(5)

# %% [markdown]
# ## Bottom Performing Schools (By % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by='% Overall Passing', ascending = True)
bottom_schools.head(5)

# %% [markdown]
# ## Math Scores by Grade

# %%
# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grade_math_scores = ninth_graders.groupby('school_name')['math_score'].mean()
tenth_grader_math_scores = tenth_graders.groupby('school_name')['math_score'].mean()
eleventh_grader_math_scores = eleventh_graders.groupby('school_name')['math_score'].mean()
twelfth_grader_math_scores = twelfth_graders.groupby('school_name')['math_score'].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.merge(pd.merge(pd.merge(ninth_grade_math_scores, tenth_grader_math_scores, on='school_name'), 
                                eleventh_grader_math_scores, on='school_name'), twelfth_grader_math_scores, on='school_name')

# Minor data wrangling
math_scores_by_grade.index.name = None
math_scores_by_grade.rename(columns={math_scores_by_grade.columns[0]: '9th', math_scores_by_grade.columns[1]: '10th',
                                     math_scores_by_grade.columns[2]: '11th', math_scores_by_grade.columns[3]: '12th'}, inplace=True)

# Display the DataFrame
math_scores_by_grade

# %% [markdown]
# ## Reading Score by Grade 

# %%
# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = ninth_graders.groupby('school_name')['reading_score'].mean()
tenth_grader_reading_scores = tenth_graders.groupby('school_name')['reading_score'].mean()
eleventh_grader_reading_scores = eleventh_graders.groupby('school_name')['reading_score'].mean()
twelfth_grader_reading_scores = twelfth_graders.groupby('school_name')['reading_score'].mean()

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.merge(pd.merge(pd.merge(ninth_grade_reading_scores, tenth_grader_reading_scores, on='school_name'),
                                            eleventh_grader_reading_scores, on='school_name'), twelfth_grader_reading_scores, on='school_name')

# Minor data wrangling
#reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None
reading_scores_by_grade.rename(columns={reading_scores_by_grade.columns[0]: '9th', reading_scores_by_grade.columns[1]: '10th',
                                        reading_scores_by_grade.columns[2]: '11th', reading_scores_by_grade.columns[3]: '12th'}, inplace=True)

# Display the DataFrame
reading_scores_by_grade

# %% [markdown]
# ## Scores by School Spending

# %%
# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# %%
# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summaryraw.copy()

# %%
# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(school_spending_df['Per Student Budget'], spending_bins, labels=labels)
school_spending_df["Total School Budget"] = school_spending_df["Total School Budget"].map("${:,.2f}".format)
school_spending_df["Per Student Budget"] = school_spending_df["Per Student Budget"].map("${:,.2f}".format)
school_spending_df

# %%
#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()
overall_passing_spending

# %%
# Assemble into DataFrame
spending_summary = pd.merge(pd.merge(pd.merge(pd.merge(spending_math_scores, spending_reading_scores, on='Spending Ranges (Per Student)'),
                                                               spending_passing_math, on='Spending Ranges (Per Student)'), spending_passing_reading, on='Spending Ranges (Per Student)'),
                                                               overall_passing_spending, on='Spending Ranges (Per Student)')

# Display results
spending_summary

# %% [markdown]
# ## Scores by School Size

# %%
# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels2 = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# %%
# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary['Total Students'], size_bins, labels=labels2)
per_school_summary

# %%
# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()

# %%
# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.merge(pd.merge(pd.merge(pd.merge(size_math_scores, size_reading_scores, on='School Size'),
                                          size_passing_math, on='School Size'), size_passing_reading, on='School Size'),
                                          size_overall_passing, on='School Size')

# Display results
size_summary

# %% [markdown]
# ## Scores by School Type

# %%
# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()

# %%
# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.merge(pd.merge(pd.merge(pd.merge(average_math_score_by_type, average_reading_score_by_type, on='School Type'),
                                          average_percent_passing_math_by_type, on='School Type'), average_percent_passing_reading_by_type, on='School Type'),
                                          average_percent_overall_passing_by_type, on='School Type') 

# Display results
type_summary

# %%



