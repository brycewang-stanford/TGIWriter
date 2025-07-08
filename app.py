from flask import Flask, render_template, request, jsonify
import openai
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/toefl')
def toefl():
    return render_template('toefl.html')

@app.route('/gre')
def gre():
    return render_template('gre.html')

@app.route('/ielts')
def ielts():
    return render_template('ielts.html')

@app.route('/generate_sample', methods=['POST'])
def generate_sample():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Use LangChain to call GPT-4 with a detailed prompt
    detailed_prompt = f"""
    You are an expert TOEFL writing instructor and rater.

    Please write a **high-scoring TOEFL Independent Writing essay** (maximum score: 5) based on the following writing prompt. The essay should demonstrate the qualities of a top-scoring response according to the official TOEFL scoring rubric.

    ### TOEFL Independent Writing Prompt:
    {prompt}

    ### Scoring Criteria:
    - **Development**: The essay presents a clear and well-supported position.
    - **Organization**: Ideas are logically ordered and fully developed with clear transitions.
    - **Language Use**: Displays consistent control of grammatical structures and vocabulary, with minimal errors.
    - **Mechanics**: Correct spelling, punctuation, and sentence formation.
    - **Length**: Around 350–400 words.

    Generate an essay that would receive a full score (5/5) from TOEFL raters.
    """

    llm = OpenAI(model="gpt-4o-mini")
    response = llm.invoke(detailed_prompt)

    # Clean and format the response
    def format_essay(text):
        # Remove any prompt content if it exists
        if "**Prompt:**" in text:
            text = text.split("**Essay:**")[-1] if "**Essay:**" in text else text.split("**Prompt:**")[-1]
        
        # Also try to remove other common markers
        if "Essay:" in text and not "**Essay:**" in text:
            text = text.split("Essay:")[-1]
        
        # Clean up the text
        text = text.strip()
        
        # More aggressive cleaning - remove all markdown formatting
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines, headers, and formatting markers
            if (line and 
                not line.startswith('**') and 
                not line.startswith('#') and
                not line.startswith('---') and
                line != "Essay:" and
                line != "Prompt:" and
                not line.startswith("Prompt:") and
                len(line) > 10):  # Only substantial content
                # Remove markdown formatting from the line
                line = line.replace('**', '').replace('*', '').replace('_', '')
                cleaned_lines.append(line)
        
        # Join all lines and then split into logical paragraphs
        full_text = ' '.join(cleaned_lines)
        
        # Split into sentences and group into paragraphs
        import re
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        paragraphs = []
        current_paragraph = []
        sentence_count = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                current_paragraph.append(sentence)
                sentence_count += 1
                
                # Create a new paragraph every 3-4 sentences
                if sentence_count >= 3 and len(current_paragraph) > 0:
                    paragraph_text = ' '.join(current_paragraph)
                    if len(paragraph_text) > 50:  # Ensure substantial content
                        paragraphs.append(paragraph_text)
                    current_paragraph = []
                    sentence_count = 0
        
        # Add remaining sentences as final paragraph
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if len(paragraph_text) > 50:
                paragraphs.append(paragraph_text)
        
        # If we still don't have good paragraphs, use the original text
        if len(paragraphs) == 0:
            paragraphs = [full_text] if len(full_text) > 50 else ["Essay content could not be properly formatted."]
        
        # Create formatted HTML
        essay_html = """
        <div class="essay-container" style="
            font-family: 'Georgia', serif; 
            line-height: 1.8; 
            max-width: 800px; 
            margin: 20px auto; 
            padding: 30px; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #4F46E5;
        ">
            <h3 style="color: #4F46E5; margin-bottom: 20px; font-size: 1.2em;">Generated TOEFL Essay</h3>
        """
        
        for i, paragraph in enumerate(paragraphs):
            essay_html += f"""
            <p style="
                margin-bottom: 18px; 
                text-align: justify; 
                color: #374151; 
                font-size: 16px;
                text-indent: {2 if i > 0 else 0}em;
            ">{paragraph}</p>
            """
        
        essay_html += "</div>"
        return essay_html

    formatted_response = format_essay(response)
    return jsonify({"sample": formatted_response})

@app.route('/score_essay', methods=['POST'])
def score_essay():
    essay_text = request.json.get('essay')
    original_prompt = request.json.get('prompt')
    
    if not essay_text or not original_prompt:
        return jsonify({"error": "Essay text and prompt are required"}), 400

    # Create a detailed scoring prompt
    scoring_prompt = f"""
    You are an expert TOEFL writing rater. Please evaluate the following essay based on the official TOEFL Independent Writing scoring rubric.

    ### Original Writing Prompt:
    {original_prompt}

    ### Essay to Score:
    {essay_text}

    ### TOEFL Scoring Rubric (Scale: 0-5):

    **Score 5 (Excellent):**
    - Effectively addresses the topic and task
    - Well organized and well developed, using clearly appropriate explanations, exemplifications, and/or details
    - Displays unity, progression, and coherence
    - Displays consistent facility in the use of language, demonstrating syntactic variety and range of vocabulary

    **Score 4 (Good):**
    - Addresses the topic and task well, though some points may not be fully elaborated
    - Generally well organized and well developed, using appropriate and sufficient explanations, exemplifications, and/or details
    - Displays unity, progression, and coherence, though it may contain occasional redundancy, digression, or unclear connections
    - Displays facility in the use of language, demonstrating syntactic variety and range of vocabulary, though it will probably have occasional noticeable minor errors

    **Score 3 (Fair):**
    - Addresses the topic and task using somewhat developed explanations, exemplifications, and/or details
    - Displays unity, progression, and coherence, though connection of ideas may be occasionally obscured
    - May demonstrate inconsistent facility in sentence formation and word choice that may result in lack of clarity and occasionally obscure meaning

    **Score 2 (Limited):**
    - Limited development in response to the topic and task
    - Inadequate organization or connection of ideas
    - Inappropriate or insufficient exemplifications, explanations, or details to support or illustrate generalizations
    - An accumulation of errors in sentence structure and/or usage

    **Score 1 (Seriously Flawed):**
    - Serious disorganization or underdevelopment
    - Little or no detail, or irrelevant specifics, or questionable responsiveness to the task
    - Serious and frequent errors in sentence structure or usage

    Please provide:
    1. **Overall Score** (0-5)
    2. **Detailed Analysis** for each criterion:
       - Task Response (how well it addresses the prompt)
       - Organization (structure, coherence, transitions)
       - Language Use (vocabulary, sentence variety, grammar)
       - Development (examples, explanations, details)
    3. **Strengths** of the essay
    4. **Areas for Improvement**
    5. **Justification** for the score given

    Format your response clearly with section headers.
    """

    llm = OpenAI(model="gpt-4o-mini")
    scoring_response = llm.invoke(scoring_prompt)
    
    # Format the scoring response
    def format_scoring(text):
        import re
        text = text.strip()
        
        # Remove markdown formatting more thoroughly
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *italic*
        text = re.sub(r'_([^_]+)_', r'\1', text)        # Remove _underline_
        text = re.sub(r'#{1,6}\s*', '', text)           # Remove markdown headers
        
        # Split into lines and clean
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3 and not line.startswith('---'):
                cleaned_lines.append(line)
        
        # More robust section detection
        sections = []
        current_section = {"title": "", "content": []}
        
        # Keywords that typically indicate section headers
        section_keywords = [
            'OVERALL SCORE', 'DETAILED ANALYSIS', 'TASK RESPONSE', 
            'ORGANIZATION', 'LANGUAGE USE', 'DEVELOPMENT', 
            'STRENGTHS', 'AREAS FOR IMPROVEMENT', 'JUSTIFICATION',
            'SCORE:', 'ANALYSIS', 'WEAKNESS', 'RECOMMENDATION'
        ]
        
        for line in cleaned_lines:
            line_upper = line.upper()
            is_header = False
            
            # Check if line is a section header
            if (line.endswith(':') and len(line) < 60) or \
               any(keyword in line_upper for keyword in section_keywords) or \
               (re.match(r'^\d+\.', line.strip()) and len(line) < 80):
                is_header = True
            
            if is_header:
                # Save previous section if it has content
                if current_section["title"] or current_section["content"]:
                    sections.append(current_section.copy())
                
                # Start new section
                current_section = {"title": line, "content": []}
            else:
                # Add to current section content
                if line:
                    current_section["content"].append(line)
        
        # Add the last section
        if current_section["title"] or current_section["content"]:
            sections.append(current_section)
        
        # If no sections were found, treat the whole text as one section
        if not sections:
            sections = [{"title": "Essay Analysis", "content": cleaned_lines}]
        
        # Create formatted HTML
        scoring_html = """
        <div class="scoring-container" style="
            font-family: 'Georgia', serif; 
            line-height: 1.8; 
            max-width: 800px; 
            margin: 20px auto; 
            padding: 30px; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #059669;
        ">
            <h3 style="color: #059669; margin-bottom: 20px; font-size: 1.2em; font-weight: bold;">📊 Essay Scoring & Analysis</h3>
        """
        
        for section in sections:
            # Add section title if exists
            if section["title"]:
                title = section["title"]
                title_color = "#374151"  # Default color
                
                # Special color for overall score
                if any(keyword in title.upper() for keyword in ['OVERALL SCORE', 'SCORE:']):
                    score_match = re.search(r'(\d+)', title)
                    if score_match:
                        score = int(score_match.group(1))
                        if score >= 4:
                            title_color = "#059669"  # Green for high scores
                        elif score <= 3:
                            title_color = "#DC2626"  # Red for low scores
                
                scoring_html += f"""
                <h4 style="
                    color: {title_color}; 
                    font-size: 1.1em; 
                    margin: 20px 0 12px 0; 
                    padding-bottom: 6px;
                    border-bottom: 2px solid #e0f2fe;
                    font-weight: bold;
                ">{title}</h4>
                """
            
            # Add section content
            if section["content"]:
                # Join content and create readable paragraphs
                full_content = ' '.join(section["content"])
                
                # Simple paragraph splitting - split on double spaces or long sentences
                paragraphs = []
                sentences = re.split(r'(?<=[.!?])\s+', full_content)
                
                current_para = []
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence:
                        current_para.append(sentence)
                        # Create new paragraph every 2-3 sentences or when reaching reasonable length
                        if len(current_para) >= 2 and len(' '.join(current_para)) > 80:
                            paragraphs.append(' '.join(current_para))
                            current_para = []
                
                # Add remaining sentences
                if current_para:
                    paragraphs.append(' '.join(current_para))
                
                # If no good paragraphs formed, use the full content as one paragraph
                if not paragraphs:
                    paragraphs = [full_content]
                
                # Generate HTML for paragraphs
                for para in paragraphs:
                    if para.strip() and len(para.strip()) > 10:
                        scoring_html += f"""
                        <p style="
                            margin-bottom: 14px; 
                            color: #374151; 
                            font-size: 15px;
                            line-height: 1.7;
                            font-weight: normal;
                            text-align: justify;
                        ">{para.strip()}</p>
                        """
        
        scoring_html += "</div>"
        return scoring_html
    
    formatted_scoring = format_scoring(scoring_response)
    return jsonify({"scoring": formatted_scoring})

@app.route('/analyze_writing', methods=['POST'])
def analyze_writing():
    essay_text = request.json.get('essay')
    
    if not essay_text:
        return jsonify({"error": "Essay text is required"}), 400

    # Enhanced analysis prompt with TOEFL-specific focus
    analysis_prompt = f"""
    You are a world-class TOEFL writing instructor and educational technology expert with over 15 years of experience. Your task is to provide comprehensive, real-time feedback on student writing with the precision and expertise of official ETS TOEFL raters.

    ### Essay Text to Analyze:
    "{essay_text}"

    ### Analysis Requirements:
    Please provide detailed, educational feedback in the following JSON structure. Be thorough, specific, pedagogically sound, and encourage student improvement.

    {{
        "spelling_errors": [
            {{"word": "misspelled_word", "suggestions": ["correct1", "correct2", "correct3"], "position": 45, "context": "surrounding sentence context", "severity": "high|medium|low"}}
        ],
        "grammar_issues": [
            {{"issue": "Subject-verb agreement error", "text": "exact problematic phrase", "suggestion": "corrected version", "position": 120, "severity": "high|medium|low", "explanation": "Detailed explanation of the grammar rule"}}
        ],
        "vocabulary_highlights": [
            {{"word": "sophisticated_word", "reason": "Demonstrates advanced academic vocabulary", "position": 200, "type": "academic|advanced|precise|domain-specific", "toefl_level": "high|medium"}}
        ],
        "sentence_structure": [
            {{"text": "complex sentence example", "feedback": "Excellent use of subordinate clauses", "position": 300, "type": "complex|compound|compound-complex|varied", "toefl_score_impact": "positive|neutral"}}
        ],
        "transitions": [
            {{"text": "transition phrase", "feedback": "Effectively connects ideas between paragraphs", "position": 150, "type": "excellent|good|adequate", "function": "contrast|addition|conclusion|causation|comparison|temporal"}}
        ],
        "weaknesses": [
            {{"text": "problematic phrase or sentence", "issue": "Unclear pronoun reference", "suggestion": "Specific, actionable improvement advice", "position": 400, "impact": "clarity|coherence|vocabulary|grammar|flow"}}
        ],
        "strengths": [
            {{"text": "excellent phrase/sentence", "reason": "Demonstrates clear argumentation", "position": 250, "category": "argumentation|vocabulary|structure|development|clarity"}}
        ],
        "coherence_analysis": [
            {{"issue": "Missing logical connection between ideas", "suggestion": "Add transitional phrase to clarify relationship", "paragraph": 2, "severity": "high|medium|low"}}
        ],
        "development_feedback": [
            {{"aspect": "examples|details|elaboration|support|explanation", "comment": "Specific observation about idea development", "suggestion": "Concrete advice for improvement"}}
        ],
        "toefl_specific_tips": [
            {{"category": "task_response|organization|language_use|development", "tip": "TOEFL-specific strategic advice", "priority": "high|medium|low"}}
        ],
        "suggestions": [
            "Prioritized, actionable improvement suggestions that will have the most impact on TOEFL score"
        ],
        "overall_assessment": {{
            "word_count_feedback": "Assessment of word count appropriateness for TOEFL (aim for 300-400 words)",
            "essay_structure": "Analysis of introduction-body-conclusion structure and paragraph organization", 
            "argument_strength": "Assessment of argument development, position clarity, and supporting evidence quality",
            "estimated_toefl_band": "Estimated score range 1-5 with detailed justification based on TOEFL rubric"
        }}
    }}

    ### Comprehensive Analysis Focus Areas:

    **1. Language Mechanics (Critical for TOEFL Success)**:
    - Spelling accuracy (especially academic vocabulary)
    - Subject-verb agreement consistency
    - Verb tense usage and consistency
    - Article usage (a/an/the) - common TOEFL challenge
    - Preposition accuracy
    - Plural/singular agreement
    - Word form errors (noun/adjective/adverb/verb forms)
    - Pronoun reference clarity
    - Parallel structure in lists and comparisons

    **2. Vocabulary Assessment (25% of TOEFL Writing Score)**:
    - Academic vocabulary sophistication
    - Word choice precision and appropriateness
    - Collocation accuracy (natural word combinations)
    - Vocabulary variety and range demonstration
    - Domain-specific terminology usage
    - Repetition avoidance strategies
    - Idiomatic expression usage
    - Register appropriateness (formal academic style)

    **3. Sentence Structure Analysis (25% of TOEFL Writing Score)**:
    - Sentence variety (simple, compound, complex, compound-complex)
    - Grammatical complexity demonstration
    - Sentence length variation for rhythm
    - Coordination and subordination balance
    - Parallel structure maintenance
    - Fragment or run-on sentence detection
    - Effective use of punctuation
    - Clause structure sophistication

    **4. Coherence & Cohesion (25% of TOEFL Writing Score)**:
    - Logical progression of ideas
    - Effective transition word usage
    - Paragraph unity and focus
    - Reference and substitution patterns
    - Repetition and variation balance
    - Overall text connectivity
    - Signposting and discourse markers
    - Logical relationship clarity

    **5. TOEFL Task Response (25% of TOEFL Writing Score)**:
    - Clear position statement (thesis)
    - Complete task requirement fulfillment
    - Argument development depth
    - Supporting example relevance and specificity
    - Counter-argument acknowledgment (if appropriate)
    - Conclusion effectiveness and summary
    - Topic adherence throughout
    - Opinion clarity and consistency

    **6. Content Development & Support**:
    - Main idea development depth
    - Supporting detail quality and relevance
    - Example specificity and appropriateness
    - Explanation clarity and logic
    - Evidence strength and credibility
    - Personal experience integration
    - Cultural awareness and sensitivity

    ### TOEFL Scoring Criteria Alignment:
    - **Score 5 (Good)**: Effectively addresses topic with well-developed response
    - **Score 4 (Fair)**: Generally addresses topic with adequate development  
    - **Score 3 (Limited)**: Addresses topic with limited development
    - **Score 2 (Inadequate)**: Limited development and organization
    - **Score 1 (Seriously Flawed)**: Serious organizational problems

    ### Quality Standards for Analysis:
    - Provide specific, actionable feedback with clear examples
    - Include educational explanations, not just corrections
    - Focus on high-impact improvements for TOEFL success
    - Consider official TOEFL scoring rubric criteria
    - Balance encouragement with constructive criticism
    - Prioritize errors by severity and score impact
    - Suggest specific strategies for improvement
    - Use encouraging, professional tone throughout

    ### Important Notes:
    - Focus on patterns, not isolated errors
    - Highlight both strengths and areas for improvement
    - Provide context for why feedback matters for TOEFL
    - Suggest specific study strategies when appropriate
    - Consider the writer's apparent proficiency level
    - Emphasize transferable skills for academic writing

    Return ONLY the JSON object with comprehensive analysis. Ensure all fields are properly filled with relevant, specific feedback. No additional text, markdown, or explanations outside the JSON structure.
    """

    llm = OpenAI(model="gpt-4o-mini")
    response = llm.invoke(analysis_prompt)
    
    try:
        # Enhanced JSON parsing with multiple fallback strategies
        import json
        import re
        
        # Remove any markdown formatting and extra text
        clean_response = response.strip()
        
        # Remove markdown code blocks
        if clean_response.startswith('```json'):
            clean_response = clean_response.replace('```json', '').replace('```', '').strip()
        elif clean_response.startswith('```'):
            clean_response = clean_response.replace('```', '').strip()
        
        # Try to extract JSON from the response using multiple patterns
        json_patterns = [
            r'\{.*\}',  # Basic JSON object
            r'\{[\s\S]*\}',  # JSON with newlines
        ]
        
        parsed_data = None
        for pattern in json_patterns:
            json_match = re.search(pattern, clean_response, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group(0))
                    break
                except json.JSONDecodeError:
                    continue
        
        if parsed_data:
            # Validate and enhance the response structure
            enhanced_analysis = validate_and_enhance_analysis(parsed_data, essay_text)
            return jsonify({"analysis": enhanced_analysis})
        else:
            raise json.JSONDecodeError("No valid JSON found", clean_response, 0)
    
    except (json.JSONDecodeError, Exception) as e:
        # Enhanced fallback with basic analysis
        fallback_analysis = generate_fallback_analysis(essay_text)
        return jsonify({"analysis": fallback_analysis})

def validate_and_enhance_analysis(data, essay_text):
    """Validate and enhance the AI analysis response"""
    
    # Ensure all required fields exist
    required_fields = [
        'spelling_errors', 'grammar_issues', 'vocabulary_highlights',
        'sentence_structure', 'transitions', 'weaknesses', 'strengths',
        'suggestions'
    ]
    
    for field in required_fields:
        if field not in data:
            data[field] = []
    
    # Add optional enhanced fields if missing
    if 'coherence_analysis' not in data:
        data['coherence_analysis'] = []
    
    if 'development_feedback' not in data:
        data['development_feedback'] = []
    
    if 'toefl_specific_tips' not in data:
        data['toefl_specific_tips'] = []
    
    if 'overall_assessment' not in data:
        data['overall_assessment'] = {
            "word_count_feedback": f"Current word count: {len(essay_text.split())} words",
            "essay_structure": "Structure analysis pending",
            "argument_strength": "Argument development assessment pending",
            "estimated_toefl_band": "Analysis in progress"
        }
    
    # Enhance suggestions if they're too generic
    if len(data['suggestions']) < 3:
        data['suggestions'].extend([
            "Vary your sentence structures to demonstrate language proficiency",
            "Include specific examples to support your main arguments",
            "Use transition words to improve coherence between paragraphs"
        ])
    
    return data

def generate_fallback_analysis(essay_text):
    """Generate basic analysis when AI parsing fails"""
    
    words = essay_text.split()
    word_count = len(words)
    sentence_count = len([s for s in essay_text.split('.') if s.strip()])
    
    return {
        "spelling_errors": [],
        "grammar_issues": [],
        "vocabulary_highlights": [],
        "sentence_structure": [],
        "transitions": [],
        "weaknesses": [],
        "strengths": [
            {
                "text": "essay completion",
                "reason": "Successfully completed the writing task",
                "position": 0,
                "category": "task_completion"
            }
        ],
        "coherence_analysis": [],
        "development_feedback": [
            {
                "aspect": "word_count",
                "comment": f"Your essay contains {word_count} words",
                "suggestion": "Aim for 300-400 words for optimal TOEFL scoring" if word_count < 300 else "Good word count for TOEFL requirements"
            }
        ],
        "toefl_specific_tips": [
            {
                "category": "general",
                "tip": "Continue writing to receive detailed AI feedback on your essay",
                "priority": "medium"
            }
        ],
        "suggestions": [
            "Keep writing to unlock detailed AI analysis",
            "Aim for clear paragraph structure with topic sentences",
            "Use specific examples to support your arguments",
            "Include transition words to connect your ideas"
        ],
        "overall_assessment": {
            "word_count_feedback": f"Current word count: {word_count} words - {'Good length' if 300 <= word_count <= 500 else 'Consider expanding' if word_count < 300 else 'Consider condensing'}",
            "essay_structure": "Basic structure assessment available after detailed analysis",
            "argument_strength": "Argument development will be analyzed with more content",
            "estimated_toefl_band": "Estimated score available after comprehensive analysis"
        }
    }

if __name__ == '__main__':
    app.run(debug=True, port=5002)
