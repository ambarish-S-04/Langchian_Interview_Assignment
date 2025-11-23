import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

def get_character_info(character_name: str) -> Dict[str, Any]:
    load_dotenv('api.env')
    
    if not os.getenv("MISTRAL_API_KEY"):
        raise ValueError("MISTRAL_API_KEY environment variable not set")
    
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )
    
    persist_directory = "vectorstore"
    try:
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    except Exception as e:
        return {"error": "Vector store not found. Please run 'compute-embeddings' first."}
    
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(character_name)
    
    if not docs:
        return {"error": "Character not found"}
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    if character_name.lower() not in context.lower():
        return {"error": "Character not found"}
    
    story_title = "Unknown Story"
    if docs and hasattr(docs[0], 'metadata') and 'source' in docs[0].metadata:
        source_path = docs[0].metadata['source']
        story_title = Path(source_path).stem
    
    prompt_template = """You are an information extraction assistant.
Given the story context below, extract structured information about the character "{character}".
The story title is: "{story_title}"

CRITICAL RULES - FOLLOW EXACTLY:
1. If the character "{character}" is NOT mentioned in the context, respond with: {{"error": "Character not found"}}
2. ONLY use information explicitly stated in the provided context
3. Do NOT infer, assume, or create any information not in the text
4. Use the story title provided above: "{story_title}"
5. Output MUST be a valid JSON object with EXACTLY these 5 fields:
   - name: (character's name as string)
   - storyTitle: (the story title provided above as string)
   - summary: (brief description of the character as string)
   - relations: (array of objects, each with "name" and "relation" fields)
   - characterType: (protagonist/antagonist/supporting character as string)

Example output format:
{{
  "name": "Jon Snow",
  "storyTitle": "A Song of Ice and Fire",
  "summary": "Jon Snow is a brave and honorable leader who serves as the Lord Commander of the Night's Watch and later unites the Free Folk and Westeros against the threat of the White Walkers.",
  "relations": [
    {{"name": "Arya Stark", "relation": "Sister"}},
    {{"name": "Eddard Stark", "relation": "Father"}}
  ],
  "characterType": "Protagonist"
}}

Context:
{context}"""

    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    llm = ChatMistralAI(
        model="mistral-tiny",
        temperature=0.2,
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "character": character_name,
            "context": context,
            "story_title": story_title
        })
        
        result = response.content.strip()
        
        try:
            parsed_result = json.loads(result)
            return parsed_result
        except json.JSONDecodeError:
            try:
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                elif "```" in result:
                    json_str = result.split("```")[1].split("```")[0].strip()
                    return json.loads(json_str)
                else:
                    return {"raw_response": result}
            except (IndexError, json.JSONDecodeError):
                return {"raw_response": result}
    except Exception as e:
        return {
            "error": f"Error processing character information: {str(e)}"
        }