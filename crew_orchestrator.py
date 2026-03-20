import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import github_analyst, job_market_agent, course_advisor_agent, synthesis_agent, roadmap_agent
from tasks import analyze_github_task, search_jobs_task, discover_courses_task, synthesize_gaps_task, generate_roadmap_task

load_dotenv()

def run_skillbridge_crew(github_url: str, career_goal: str):
    """
    Initializes and runs the CrewAI multi-agent Orchestration.
    """
    
    # We create the Crew
    skillbridge_crew = Crew(
        agents=[
            github_analyst,
            job_market_agent,
            course_advisor_agent,
            synthesis_agent,
            roadmap_agent
        ],
        tasks=[
            analyze_github_task,
            search_jobs_task,
            discover_courses_task,
            synthesize_gaps_task,
            generate_roadmap_task
        ],
        process=Process.sequential,  # For MVP, sequential is easiest to manage and debug
        verbose=True
    )
    
    inputs = {
        'github_url': github_url,
        'career_goal': career_goal
    }
    
    # Run the crew
    result = skillbridge_crew.kickoff(inputs=inputs)
    
    # Helper to safely get task output
    def get_output(task, default):
        if not getattr(task, 'output', None): return default
        return getattr(task.output, 'raw', getattr(task.output, 'raw_output', str(task.output)))

    # Extract intermediate outputs for the UI
    github_output = get_output(analyze_github_task, "No GitHub output.")
    gaps_output = get_output(synthesize_gaps_task, "No synthesis output.")
    roadmap_output = get_output(generate_roadmap_task, str(result))
    
    return {
        "github_analysis": github_output,
        "skill_gaps": gaps_output,
        "roadmap": roadmap_output
    }
