import json
import os
import requests
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class GithubAnalyzerInput(BaseModel):
    github_url: str = Field(..., description="The GitHub profile URL of the student.")

class GithubAnalyzerTool(BaseTool):
    name: str = "GitHub Profile Analyzer"
    description: str = "Analyzes a given GitHub profile URL and extracts the programming languages, frameworks, and skills demonstrated in the user's public repositories."
    args_schema: Type[BaseModel] = GithubAnalyzerInput

    def _run(self, github_url: str) -> str:
        # Extract username from URL
        # e.g., https://github.com/mitch
        username = github_url.strip("/").split("/")[-1]
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
            
        repos = []
        page = 1
        print(f"\n--- Fetching all public repositories for {username} ---")
        while True:
            repo_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&sort=updated"
            try:
                response = requests.get(repo_url, headers=headers)
                if response.status_code == 200:
                    page_repos = response.json()
                    if not page_repos:
                        break
                    repos.extend(page_repos)
                    page += 1
                else:
                    return f"Could not fetch repos for {username}. Status Code: {response.status_code}."
            except Exception as e:
                return f"Error connecting to GitHub API for {username}: {str(e)}."

        print(f"Found {len(repos)} public repositories:")
        languages = set()
        topics = set()
        project_descriptions = []
        
        for repo in repos:
            print(f" - {repo.get('html_url')}")
            if repo.get("language"):
                languages.add(repo["language"])
            if repo.get("topics"):
                topics.update(repo["topics"])
            if repo.get("description"):
                project_descriptions.append(repo["description"])
        print("--------------------------------------------------\n")
        
        return f"""GitHub Analysis for {username}:
- Total Repositories Analyzed: {len(repos)}
- Primary Languages: {', '.join(filter(None, languages))}
- Topics / Frameworks: {', '.join(filter(None, topics))}
- Recent Projects Snippets: {'. '.join(project_descriptions[:3])}"""


class JobSearchInput(BaseModel):
    career_goal: str = Field(..., description="The career goal or job title the student wants, e.g., 'Data Engineer'")

class JobSearchTool(BaseTool):
    name: str = "Job Market Searcher"
    description: str = "Searches for job postings related to a career goal and returns the top 10 required skills for that role."
    args_schema: Type[BaseModel] = JobSearchInput

    def _run(self, career_goal: str) -> str:
        # For a hackathon MVP, we mock the job market data based on typical roles
        goal_lower = career_goal.lower()
        
        if "data engineer" in goal_lower:
            return "Top skills for Data Engineer: Apache Spark, AWS, Airflow, SQL, Python, Hadoop, Kafka, Snowflake, Data Warehousing, CI/CD."
        elif "software engineer" in goal_lower or "developer" in goal_lower:
            return "Top skills for Software Engineer: Python, Java, JavaScript, React, System Design, Git, Docker, Kubernetes, AWS, SQL."
        elif "data scientist" in goal_lower:
            return "Top skills for Data Scientist: Python, Machine Learning, Deep Learning, SQL, PyTorch, TensorFlow, Statistics, Pandas, AWS/GCP, Data Visualization."
        else:
            return f"Top skills for {career_goal}: Python, Communication, Problem Solving, Project Management, Git, SQL, APIs, Cloud Basics, Agile, Design Patterns."


class CourseCatalogInput(BaseModel):
    query: str = Field(..., description="Keywords representing the skills the student needs to learn (e.g., 'AWS', 'Spark', 'Machine Learning').")

class CourseCatalogTool(BaseTool):
    name: str = "NCCU Course Catalog Search"
    description: str = "Searches the NCCU course catalog to find classes that teach the specific skills mentioned in the query."
    args_schema: Type[BaseModel] = CourseCatalogInput

    def _run(self, query: str) -> str:
        try:
            catalog_path = os.path.join(os.path.dirname(__file__), "data", "nccu_catalog.json")
            with open(catalog_path, "r") as f:
                catalog = json.load(f)
                
            query_skills = [skill.strip().lower() for skill in query.split(",")]
            matches = []
            
            for course in catalog:
                course_skills = [s.lower() for s in course.get("skills_covered", [])]
                # Check for overlap
                overlap = set(query_skills).intersection(set(course_skills))
                # Also check description loosely
                description = course.get("description", "").lower()
                for q in query_skills:
                    if q in description:
                        overlap.add(q)
                
                if overlap:
                    matches.append(
                        f"Course: {course['course_id']} - {course['course_name']} (Prof. {course['professor']})\n"
                        f"  Skills: {', '.join(course['skills_covered'])}\n"
                        f"  Description: {course['description']}"
                    )
            
            if matches:
                return "Matches found in NCCU Catalog:\n" + "\n".join(matches)
            else:
                return "No exact NCCU courses found for those skills. Consider self-study or online platforms."
                
        except Exception as e:
            return f"Error reading course catalog: {str(e)}"
