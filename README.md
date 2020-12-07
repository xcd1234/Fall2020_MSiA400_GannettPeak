# Fall2020_MSiA400_GannettPeak
Group Members: Jun-yong Choi, Seok Hyun Kim, Matthew Ko, Binqi Shen, Congda Xu
Greenwich.HR project – Fall 2020

Client
Greenwich.HR (https://greenwich.hr/) is a labor market intelligence firm who seeks to connect investment managers, employers, recruiters, and business intelligence teams to valuable, real-time insights pulled from job market data. Their mission is to make it easier to understand what is happening in the job market by providing comprehensible, real-time, accurate, and accessible data. An example of one application for Greenwich.HR’s dataset can be found in the publicly-available daily job tracking site https://covidjobimpacts.greenwich.hr.

Problem
Job posting data offers a rich source of insight on companies’ future activities, since jobs are often posted, and hence publicly visible, 3-6 months before hiring takes place. Recent studies have shown that hiring data input can be used to develop models that yield over 80% correlation to future financial metrics such as EBITDA, operating margin, and gross sales.  
That said, uncovering this type of intelligence from job posting data requires some in-depth analysis, and there are many company-specific considerations that influence the nature of the obtainable signal.  For example, certain types of jobs may be more impactful on a company’s future performance than others, and therefore hiring of these jobs should be weighted more heavily.  Also, companies’ management philosophies and embedded systemic practices may heavily influence the relationship between hiring and pay behaviors and business performance.  A recent study demonstrated that in certain companies, models could be developed that showed hiring behavior to be predictive of future financial metrics, but in other companies the relationship is lagging – the opposite.
This study seeks to advance the practice of developing models that are predictive of future stock performance based on hiring data inputs that include data elements unique to the Greenwich.HR dataset.  We are targeting a specific client segment with this knowledge – quantitative investment fund managers.  The value we are seeking to deliver them is 1) further proof points that hiring data can be provide trading signals, 2) understanding of the various considerations and configuration options for the models that uncover these signals, and 3) awareness of the differentiated value of the Greenwich.HR dataset.    




Project goal: 
The goal is this project is to both define a modeling approach that yields optimal results, and also (importantly) to document in a white-paper format the project approach, findings, and conclusions that can be communicated to interested stakeholders, such as potential customers, media, economists, etc.  
Dataset: 
Data on the daily hiring and pay activities of 3400 publicly-traded companies starting in Jan 2017.
Data on companies’ stock performance and the S&P500 index daily values will also need to be obtained by teams from public sources.
 
Data Analysis goals:
Explore the relationship between hiring and pay practices and overall stock performance by:  
-	Develop and test various types of models to find a segment of companies with highest correlation between metrics from data and future stock performance.  The specific test we will be using is the ability to predict whether a given stock will outperform, match, or underperform the S&P500 90 days in the future.
o	We are seeking a model that is stable for at least 50 companies, and no fewer than 20.
o	Teams will be free to define appropriate input vectors of metrics, but those metrics must include at least one pay metric and preferably one job feature metric (the configuration of input vectors will be discussed during the project kickoff).  
-	Simulate a trading strategy where a portfolio of the identified companies is re-balanced daily, weekly, and monthly based on model predictions, to test the portfolio’s performance against the S&P500 index performance.
-	Document project approach, findings, and conclusions in a white-paper format suitable for publishing in blog and business-press channels (note this is a mandatory deliverable).
This project can be conducted by any number of teams.  Teams are free to choose modeling approaches and input strategies, subject to above requirements.  
Competition
The team who can successfully create a trading strategy that best outperforms the S&P500 benchmark is eligible for a modest award.  In order to qualify for the award, the team must:
•	Successfully complete all project deliverables within the time allotted
•	Develop a modeling and simulation approach that meets the goals of this project and is verified as valid and accurate by course faculty
•	Identify a trading strategy demonstrated to outperform the S&P500 index by at least % for the analysis period, and beat the performance of all other teams’ strategies

