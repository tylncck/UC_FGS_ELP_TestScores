# Multinomial Analysis of ELP Tests and Cumulative GPA

* **Author:** Taylan Cicek
* **Institution:** University of Calgary - Faculty of Graduate Studies
* **Contact:** onurtaylan.cicek@ucalgary.ca

Welcome to the analysis of student GPAs with respect to their English Language Proficiency (ELP) test submissions. This project aims to test if Cumulative GPA of students differ from each other with respect to the English Language Proficiency Tests they submitted. 

## Table of Contents

- [Background](#background)

- [Methodology](#methodology)

- [Installation](#installation)

- [Usage](#usage)

- [Results](#results)

- [License](#license)

## Background

English language proficiency is a crucial factor for academic success, particularly in English-speaking educational institutions. As such, understanding the relationship between students' preference of ELP tests and their academic outcomes, such as GPAs, is of great importance. In this analysis, I aim to investigate whether there are significant differences in student GPAs based on the ELP test they submitted. The outcome will support the decision of continuation of some test types or not. 

## Methodology

### Data Preprosessing

Before implementing statistical tests, the dataset was preprocessed to ensure the validity of the analysis:
- Outliers were identified and filtered out from the dataset to prevent their influence on the results.
- Statistical tests were complemented with exploratory data analysis (EDA), including visualizations, to gain insights into the distribution and relationships of the variables.

### Testing Assumptions of ANOVA Test

The analysis involved using ANOVA to compare means across multiple groups. ANOVA assumes the following:

- Independence of observations: Each observation in the dataset is independent of others.
- Normality: The dependent variable follows a normal distribution within each group.
- Homogeneity of variances (homoscedasticity): The variance of the dependent variable is equal across all groups.

### Statistical Tests

Statistical tests were conducted to assess differences in GPA distributions among the ELP test categories:

- **Normality Test:** Shapiro-Wilk test was initially performed to assess the normality of GPA distributions within each ELP test category. The test was conducted both before and after applying Box-Cox transformation to the data.
- **Homogeneity of Variances Test:** Bartlett test was conducted to assess the homogeneity of variances assumption required for ANOVA. 
- **ANOVA Test:** ANOVA was initially planned to compare means across multiple ELP test categories. However, due to non-normality of GPA distributions parametric ANOVA was not appropriate. *Just to observe the outcome, ANOVA test, which was followed by pairwise Bonferroni corrected t-tests were implemented*
- **Kruskal-Wallis Test:** Instead, Kruskal-Wallis test, a non-parametric alternative to ANOVA, was conducted to compare distributions across multiple groups.
- **Post-hoc Pairwise Comparisons:** Following significant results from the Kruskal-Wallis test, post-hoc pairwise comparisons using Mann-Whitney U test were conducted to identify specific differences in GPAs between individual ELP test categories.

Additional statistical tests were implemented to determine if ELP Tests are associated with student's discontinuation to their programs. 
- **Chi-Square Test of Independence** was not appropriate to the dataset due to violation of having at least 5 observation of failure. 
- **Fisher's Exact Test** is more appropriate for datasets having small sample sizes. Therefore proportion comparisons were made using this test. 

## Installation

All required packages for this project are listed in the [requirements](requirements.txt) file and can be installed using the command `pip install -r requirements.txt` command. 

## Usage

It's important to note that the Jupyter notebook file relies on the SQL server for data retrieval. Therefore, proper authentication and VPN configurations are required to run the notebook and access the data. Ensure that the necessary credentials and network settings are in place before executing the notebook.

## Results

Mean and Median GPA comparisons resulted in:

- The majority of students prefer taking the IELTS test, while TOEFL and Duolingo are relatively uncommon among students.
- Cumulative GPA distribution of students does not adhere to a normal distribution even after Box-Cox transformation, precluding the use of parametric tests such as ANOVA.
- The homogeneity of variance in GPA across test types was confirmed.
- The Kruskal-Wallis test rejected the null hypothesis, indicating that at least one group has a different median compared to the others.
- Subsequent Mann-Whitney U tests revealed that the four test types can be grouped into three categories:
    - Group A: IELTS, with the lowest median GPA
    - Group B: No test takers
    - Group C: Tests indicate that TOEFL and Duolingo have equal median GPAs, being overall higher compared to others.

Discontinuation Rate comparisons resulted in:
- No test takers has the highest discontinuation rate and this association is statistically significant. 
- Duolingo takers statistically have same proportions with other tests. Having only 2 discontinuation our of 100 makes the judgement for Duolingo a little bit unreliable. 
- IELTS and TOEFL takers are the group having the lowest discontinuation rate.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. The MIT License is a permissive open-source license that allows you to freely use, modify, and distribute this software for any purpose, with no warranty. By using or contributing to this project, you agree to abide by the terms of the MIT License.