from crewai import Agent
from tools import GithubAnalyzerTool, JobSearchTool, CourseCatalogTool
import os

# Initialize Tools
github_tool = GithubAnalyzerTool()
job_tool = JobSearchTool()
course_tool = CourseCatalogTool()

# Define Agents
github_analyst = Agent(
    role='Lead GitHub Intelligence Analyst',
    goal='Analyze a student\'s GitHub profile ({github_url}) and extract a highly accurate inventory of their technical skills, programming languages, code quality signals, and project complexity.',
    backstory='You are a senior technical recruiter and ex-software engineer. You can look at a GitHub profile and instantly know what technologies an applicant actually uses vs. what they just claim on their resume.',
    verbose=True,
    allow_delegation=False,
    tools=[github_tool]
)

job_market_agent = Agent(
    role='Market Demand Analyst',
    goal='Identify the top 10 required skills in the current job market for the career goal: {career_goal}.',
    backstory='You are a labor market researcher specializing in tech roles. You know exactly what employers are asking for in modern job descriptions.',
    verbose=True,
    allow_delegation=False,
    tools=[job_tool]
)

course_advisor_agent = Agent(
    role='NCCU Academic Advisor',
    goal='Find the best NCCU courses and professors that teach the specific skills ({career_goal} related skills) that the student might be missing.',
    backstory='You are a knowledgeable academic advisor at NCCU. You have memorized the entire course catalog, prerequisites, and which professors teach which modern technologies.',
    verbose=True,
    allow_delegation=False,
    tools=[course_tool]
)

synthesis_agent = Agent(
    role='Skill Gap Analyst',
    goal='Compare the student\'s verified GitHub skills against the market requirements for {career_goal} and produce a prioritized list of missing skills.',
    backstory='You are a career strategist. You excel at finding the delta between what someone knows and what employers want, organizing the gaps by priority and impact.',
    verbose=True,
    allow_delegation=False
)

roadmap_agent = Agent(
    role='Action Plan Architect',
    goal='Create a highly specific, actionable, semester-by-semester learning roadmap combining NCCU courses, projects, and self-study to bridge the skill gap.',
    backstory='You are an elite career coach. You transform negative feedback (skill gaps) into an inspiring, step-by-step 6-month action plan that guarantees job readiness.',
    verbose=True,
    allow_delegation=False
)
