from crewai import Task
from agents import github_analyst, job_market_agent, course_advisor_agent, synthesis_agent, roadmap_agent

# 1. GitHub Analysis Task
analyze_github_task = Task(
    description='Analyze the GitHub profile at {github_url}. Identify the primary languages, frameworks, and infer their technical skill level based on repository descriptions and topics.',
    expected_output='A concise report listing verified technical skills, languages, and project types found on the student\'s GitHub.',
    agent=github_analyst
)

# 2. Job Market Search Task
search_jobs_task = Task(
    description='Search the current job market for the role: {career_goal}. Identify the top 10 most in-demand technical skills for this role.',
    expected_output='A prioritized list of the top 10 technical skills required for the target career goal.',
    agent=job_market_agent
)

# 3. NCCU Course Discovery Task
discover_courses_task = Task(
    description='Search the NCCU Course Catalog for courses that teach the key skills required for {career_goal}. Use keywords related to the career goal to find matches.',
    expected_output='A list of relevant NCCU courses, including course name, professor, and the specific skills covered.',
    agent=course_advisor_agent
)

# 4. Skill Gap Synthesis Task
synthesize_gaps_task = Task(
    description='Compare the student\'s verified GitHub skills (from the GitHub Analyst) against the top 10 required market skills (from the Job Market Analyst). Identify exactly what the student is missing.',
    expected_output='A clear, prioritized bulleted list of the top technical skills the student lacks compared to the market demand.',
    agent=synthesis_agent,
    context=[analyze_github_task, search_jobs_task] # Depends on the first two tasks
)

# 5. Roadmap Generation Task
generate_roadmap_task = Task(
    description='Using the identified skill gaps and the available NCCU courses (from the Course Advisor), create a 6-month, semester-by-semester learning roadmap. Include what courses to take, and suggest 1-2 specific personal projects to build the missing skills.',
    expected_output='A highly structured, markdown-formatted 6-month learning roadmap bridging the gap between current skills and the target career goal.',
    agent=roadmap_agent,
    context=[synthesize_gaps_task, discover_courses_task] # Depends on gaps and course options
)
