"""Knowledge base and retrieval system using embeddings."""

from typing import List, Optional, Dict
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import streamlit as st

from models.database import KnowledgeBase
from utils.database import get_db


class KnowledgeRetriever:
    """Retrieve relevant context from knowledge base using embeddings."""
    
    def __init__(self):
        """Initialize knowledge retriever with ChromaDB and embeddings."""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(ChromaSettings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory="./chroma_db"
        ))
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_or_create_collection(
                name="boeing_india_knowledge",
                metadata={"description": "Boeing India career information"}
            )
        except Exception as e:
            st.warning(f"ChromaDB initialization: {str(e)}")
            self.collection = None
    
    def add_knowledge(self, title: str, content: str, source: str, category: str, metadata: Optional[Dict] = None):
        """Add knowledge to the database and vector store."""
        # Save to PostgreSQL
        with get_db() as db:
            kb_entry = KnowledgeBase(
                title=title,
                content=content,
                source=source,
                category=category,
                metadata=metadata or {}
            )
            db.add(kb_entry)
            db.commit()
            db.refresh(kb_entry)
            
            # Add to ChromaDB if available
            if self.collection:
                try:
                    embedding = self.embedding_model.encode([content])[0]
                    self.collection.add(
                        embeddings=[embedding.tolist()],
                        documents=[content],
                        metadatas=[{
                            "id": kb_entry.id,
                            "title": title,
                            "source": source,
                            "category": category
                        }],
                        ids=[str(kb_entry.id)]
                    )
                except Exception as e:
                    st.warning(f"ChromaDB add error: {str(e)}")
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context for a query.
        
        Args:
            query: User's question or query
            top_k: Number of top results to retrieve
            
        Returns:
            Formatted context string
        """
        if not self.collection:
            return ""
            
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            if not results['documents'] or not results['documents'][0]:
                return ""
            
            # Format context
            context_parts = []
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                context_parts.append(f"Source {i+1} ({metadata.get('category', 'general')}): {doc}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            st.warning(f"Context retrieval error: {str(e)}")
            return ""
    
    def initialize_knowledge_base(self):
        """Initialize knowledge base with Boeing India information."""
        boeing_knowledge = [
            {
                "title": "Boeing India Overview",
                "content": """Boeing India is a significant presence of The Boeing Company in India, with operations 
spanning defense, commercial aviation, and services. Boeing has been in India for over 75 years and employs 
over 3,000 people across multiple locations including Bengaluru, Delhi, Mumbai, Chennai, and Hyderabad. 
The company focuses on aerospace manufacturing, engineering, research and development, and customer support.""",
                "source": "boeing.co.in",
                "category": "company_overview"
            },
            {
                "title": "Campus Recruitment Process",
                "content": """Boeing India conducts campus recruitment drives at premier engineering institutions 
across India. The typical process includes: 1) Online application through career portal, 2) Online aptitude 
and technical assessment, 3) Technical interviews (2-3 rounds), 4) HR interview, 5) Final offer. 
Eligible branches include Aerospace, Mechanical, Electronics, Computer Science, and related engineering fields. 
Minimum CGPA requirement is typically 7.0 or above.""",
                "source": "boeing.co.in/careers",
                "category": "placement"
            },
            {
                "title": "Internship Opportunities",
                "content": """Boeing India offers internship programs for pre-final and final year engineering students. 
Internships are available in various domains: Engineering (Design, Analysis, Manufacturing), IT and Software Development, 
Supply Chain, Quality Assurance, and Research & Development. Internships typically last 2-6 months during summer or winter breaks. 
Selected interns receive stipend and have potential for pre-placement offers (PPO) based on performance.""",
                "source": "boeing.co.in/careers/students",
                "category": "internship"
            },
            {
                "title": "Job Roles for Engineers",
                "content": """Common job roles for engineering graduates at Boeing India include: 1) Aerospace Engineer 
- aircraft design and analysis, 2) Software Engineer - avionics and embedded systems, 3) Manufacturing Engineer 
- production and assembly, 4) Systems Engineer - integration and testing, 5) Quality Engineer - quality assurance 
and compliance, 6) Supply Chain Analyst - logistics and procurement. Entry-level positions offer competitive compensation 
and comprehensive benefits.""",
                "source": "boeing.co.in/careers",
                "category": "roles"
            },
            {
                "title": "Skills Required for Boeing India",
                "content": """Key skills for Boeing India roles: Technical skills - CAD/CAM (CATIA, SolidWorks), 
Programming (C++, Python, Java), Data Analysis, Systems Engineering. Soft skills - Problem-solving, Team collaboration, 
Communication, Attention to detail. Domain knowledge - Aerospace fundamentals, Manufacturing processes, 
Safety and quality standards (AS9100, DO-178C). Certifications in Six Sigma, Project Management, or relevant 
technical areas are valued.""",
                "source": "boeing.co.in/careers",
                "category": "skills"
            },
            {
                "title": "Interview Preparation Tips",
                "content": """To prepare for Boeing India interviews: 1) Brush up on aerospace basics and aviation industry knowledge, 
2) Review engineering fundamentals in your domain, 3) Practice coding problems for software roles, 4) Prepare STAR format 
answers for behavioral questions, 5) Research Boeing's current projects in India (like Apache helicopters, P-8I aircraft), 
6) Understand Boeing's values: Safety, Quality, Integrity, 7) Prepare questions about the role and team. 
Technical rounds focus on problem-solving and domain knowledge.""",
                "source": "Career guidance",
                "category": "interview_prep"
            },
            {
                "title": "Resume Tips for Boeing Applications",
                "content": """Resume tips for Boeing India: 1) Keep it concise (1-2 pages), 2) Highlight relevant technical projects 
with measurable outcomes, 3) Include aerospace-related coursework and certifications, 4) Emphasize teamwork and leadership experiences, 
5) List technical skills with proficiency levels, 6) Use action verbs and quantify achievements, 7) Ensure error-free formatting 
and grammar, 8) Include relevant internships or industrial training, 9) Mention participation in aerospace competitions 
(SAE Aero Design, Boeing competitions), 10) Tailor resume to the specific role.""",
                "source": "Career guidance",
                "category": "resume_tips"
            },
            {
                "title": "Career Growth at Boeing India",
                "content": """Boeing India offers clear career progression paths: Entry-level engineers can grow to 
Senior Engineer (3-5 years), Lead Engineer (6-8 years), Principal Engineer (10+ years), and management roles. 
The company provides continuous learning opportunities through Boeing Learning Together Program (education assistance), 
technical training, leadership development programs, and global exposure through international projects. 
Internal mobility allows movement across functions and locations.""",
                "source": "boeing.co.in/careers",
                "category": "career_path"
            },
            {
                "title": "Boeing India Locations and Work Culture",
                "content": """Boeing India operates from multiple locations: Bengaluru (Engineering & Technology Center, largest site), 
Delhi NCR (Regional offices), Mumbai (Commercial operations), Chennai and Hyderabad (Support offices). 
Work culture emphasizes innovation, safety-first mindset, collaboration, diversity and inclusion, and work-life balance. 
Benefits include competitive salary, health insurance, performance bonuses, flexible work arrangements, 
and employee wellness programs.""",
                "source": "boeing.co.in",
                "category": "work_culture"
            },
            {
                "title": "Project Ideas for Boeing Aspirants",
                "content": """Recommended projects for students targeting Boeing India: 1) UAV/Drone design and development, 
2) Aerodynamic analysis using CFD tools, 3) Flight simulator development, 4) Aircraft structural analysis using FEA, 
5) Avionics systems projects, 6) Manufacturing process optimization, 7) Supply chain analytics for aerospace, 
8) Quality control automation systems, 9) Predictive maintenance using ML, 10) Composite materials research. 
These projects demonstrate relevant technical skills and aerospace interest.""",
                "source": "Career guidance",
                "category": "projects"
            }
        ]
        
        # Add all knowledge to the database
        for item in boeing_knowledge:
            try:
                self.add_knowledge(**item)
            except Exception as e:
                # Skip if already exists
                pass


retriever = KnowledgeRetriever()
