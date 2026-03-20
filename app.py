import streamlit as st
import os
from crew_orchestrator import run_skillbridge_crew

st.set_page_config(page_title="SkillBridge AI", page_icon="🎯", layout="wide")

st.title("🎯 SkillBridge")
st.markdown("### Agentic Career & Learning Intelligence Platform")
st.markdown("*Bridging the gap between what you build, what employers need, and what we teach.*")

# Sidebar for Inputs
with st.sidebar:
    st.header("Applicant Input")
    github_url = st.text_input("GitHub Profile URL", "https://github.com/torvalds")
    career_goal = st.text_input("Career Goal", "Senior Systems Engineer")
    
    st.markdown("---")
    st.markdown("**Configuration**")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    run_button = st.button("Run SkillBridge Analysis", type="primary")

# Main Display Area
if run_button:
    if not api_key and not os.getenv("OPENAI_API_KEY"):
        st.error("Please provide an OpenAI API Key to run the agents.")
    elif not github_url or not career_goal:
        st.error("Please provide both a GitHub URL and a Career Goal.")
    else:
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
        with st.spinner("Agents are analyzing profile, market, and curriculum..."):
            try:
                results = run_skillbridge_crew(github_url, career_goal)
                
                # Create tabs for the output views
                tab1, tab2 = st.tabs(["🎓 Student View", "🏢 Recruiter View"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Current Skill Snapshot")
                        st.info(results["github_analysis"])
                        
                        st.subheader("Identified Skill Gaps")
                        st.warning(results["skill_gaps"])
                    
                    with col2:
                        st.subheader("Your Personalized Learning Roadmap")
                        st.success(results["roadmap"])
                        
                with tab2:
                    st.subheader("Verified Technical Signals")
                    st.write("This applicant claims to be aiming for: **" + career_goal + "**")
                    st.write("Based on their actual code repositories, we verified the following skills:")
                    st.info(results["github_analysis"])
                    
                    st.subheader("Hiring Recommendation & Risk Analysis")
                    st.write("The applicant is missing the following core competencies for this role:")
                    st.warning(results["skill_gaps"])
                    st.markdown("> **Note**: SkillBridge agents have prescribed a 6-month roadmap to close these exact gaps. Follow up in 3 months.")
            
            except Exception as e:
                st.error(f"An error occurred during agent execution: {str(e)}")
else:
    st.info("Enter your GitHub URL and Career Goal in the sidebar, then click 'Run SkillBridge Analysis'.")
