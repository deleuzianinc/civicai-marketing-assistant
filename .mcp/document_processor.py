# document_processor.py
import re
import json
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import tiktoken
from collections import Counter

class DocumentationProcessor:
    def __init__(self, embedding_model='sentence-transformers/all-mpnet-base-v2'):
        """
        Initialize the documentation processor
        
        Args:
            embedding_model: HuggingFace model name or 'openai' for OpenAI embeddings
        """
        self.embedding_model_name = embedding_model
        
        # Initialize embedding model
        if embedding_model == 'openai':
            import openai
            self.use_openai = True
            # Ensure OPENAI_API_KEY is set in environment
        else:
            self.use_openai = False
            print(f"Loading embedding model: {embedding_model}")
            self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize tokenizer for chunk size estimation
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def extract_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extract hierarchical sections from markdown documentation"""
        sections = []
        current_section = {
            'level': 0,
            'title': 'Root',
            'content': [],
            'subsections': []
        }
        section_stack = [current_section]
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for markdown headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Create new section
                new_section = {
                    'level': level,
                    'title': title,
                    'content': [],
                    'subsections': []
                }
                
                # Pop sections from stack until we find the parent
                while section_stack and section_stack[-1]['level'] >= level:
                    section_stack.pop()
                
                # Add to parent's subsections
                if section_stack:
                    section_stack[-1]['subsections'].append(new_section)
                
                section_stack.append(new_section)
            else:
                # Add content to current section
                if section_stack:
                    section_stack[-1]['content'].append(line)
        
        return [current_section]
    
    def create_chunks_with_metadata(self, content: str) -> List[Dict[str, Any]]:
        """Create semantically meaningful chunks with rich metadata"""
        chunks = []
        
        # Extract hierarchical structure
        sections = self.extract_sections(content)
        
        # Configure recursive text splitter for technical docs
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,  # Larger chunks for technical content
            chunk_overlap=200,  # Good overlap to maintain context
            length_function=len,
            separators=[
                "\n## ",      # Major sections
                "\n### ",     # Subsections
                "\n#### ",    # Sub-subsections
                "\n\n",       # Paragraphs
                "\n",         # Lines
                ". ",         # Sentences
                " ",          # Words
                ""
            ]
        )
        
        def process_section(section: Dict, parent_path: str = "") -> None:
            """Recursively process sections and create chunks"""
            section_title = section['title']
            current_path = f"{parent_path}/{section_title}" if parent_path else section_title
            
            # Join content
            section_content = '\n'.join(section['content']).strip()
            
            if section_content:
                # Extract keywords from content
                keywords = self.extract_keywords(section_content)
                
                # Split content into chunks
                text_chunks = text_splitter.split_text(section_content)
                
                for i, chunk_text in enumerate(text_chunks):
                    # Detect content type
                    content_type = self.detect_content_type(chunk_text)
                    
                    chunk_metadata = {
                        'section': section_title,
                        'section_path': current_path,
                        'section_level': section['level'],
                        'chunk_index': i,
                        'total_chunks': len(text_chunks),
                        'keywords': keywords[:10],  # Top 10 keywords
                        'content_type': content_type,
                        'char_count': len(chunk_text),
                        'estimated_tokens': len(self.tokenizer.encode(chunk_text))
                    }
                    
                    chunks.append({
                        'content': chunk_text,
                        'metadata': chunk_metadata
                    })
            
            # Process subsections
            for subsection in section.get('subsections', []):
                process_section(subsection, current_path)
        
        # Process all sections
        for section in sections:
            process_section(section)
        
        return chunks
    
    def extract_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """Extract important keywords from text"""
        # Common technical terms that should be preserved
        technical_terms = {
            'dialogflow', 'cx', 'intent', 'entity', 'webhook', 'fulfillment',
            'parameter', 'flow', 'page', 'route', 'playbook', 'agent',
            'api', 'console', 'session', 'training', 'phrases', 'nlp'
        }
        
        # Remove code blocks and special characters
        clean_text = re.sub(r'```[\s\S]*?```', '', text)
        clean_text = re.sub(r'`[^`]+`', '', clean_text)
        
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', clean_text.lower())
        
        # Common stop words to exclude
        stop_words = {
            'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from',
            'you', 'can', 'your', 'will', 'when', 'how', 'what', 'where'
        }
        
        # Filter and count
        filtered_words = [w for w in words if w not in stop_words]
        word_freq = Counter(filtered_words)
        
        # Prioritize technical terms
        keywords = []
        for word in technical_terms:
            if word in word_freq:
                keywords.append(word)
        
        # Add other frequent words
        for word, _ in word_freq.most_common(top_n):
            if word not in keywords:
                keywords.append(word)
        
        return keywords[:top_n]
    
    def detect_content_type(self, text: str) -> str:
        """Detect the type of content in the chunk"""
        if re.search(r'```[\s\S]*?```', text):
            return 'code_example'
        elif re.search(r'^#{1,6}\s', text, re.MULTILINE):
            return 'section_header'
        elif re.search(r'^\*\*[^*]+\*\*:', text, re.MULTILINE):
            return 'definition_list'
        elif re.search(r'^\d+\.', text, re.MULTILINE):
            return 'numbered_list'
        elif re.search(r'^[-*]\s', text, re.MULTILINE):
            return 'bullet_list'
        elif re.search(r'\bhttps?://\S+', text):
            return 'reference_links'
        else:
            return 'paragraph'
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for text chunks"""
        if self.use_openai:
            import openai
            embeddings = []
            for text in texts:
                response = openai.Embedding.create(
                    input=text,
                    model="text-embedding-3-small"  # or "text-embedding-ada-002"
                )
                embeddings.append(response['data'][0]['embedding'])
            return embeddings
        else:
            return self.embedding_model.encode(texts, show_progress_bar=True).tolist()
    
    def process_and_store(self, file_path: str, collection_name: str = "dialogflow_docs"):
        """Main processing pipeline"""
        print(f"Reading file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Creating chunks with metadata...")
        chunks = self.create_chunks_with_metadata(content)
        print(f"Created {len(chunks)} chunks")
        
        # Initialize ChromaDB
        print("Initializing ChromaDB...")
        client = chromadb.PersistentClient(path="./dialogflow_chroma_db")
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Dialogflow CX Documentation"}
        )
        
        # Prepare data for ChromaDB
        chunk_ids = [f"chunk_{i}" for i in range(len(chunks))]
        chunk_texts = [chunk['content'] for chunk in chunks]
        
        # Convert lists to strings in metadata for ChromaDB compatibility
        chunk_metadatas = []
        for chunk in chunks:
            metadata = chunk['metadata'].copy()
            # Convert keywords list to comma-separated string
            metadata['keywords'] = ', '.join(metadata['keywords']) if metadata['keywords'] else ''
            chunk_metadatas.append(metadata)
        
        # Create embeddings
        print("Generating embeddings...")
        embeddings = self.create_embeddings(chunk_texts)
        
        # Store in ChromaDB
        print("Storing in ChromaDB...")
        collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunk_texts,
            metadatas=chunk_metadatas
        )
        
        print(f"✅ Successfully processed and stored {len(chunks)} chunks")
        print(f"Collection '{collection_name}' now contains {collection.count()} items")
        
        # Create summary report
        self.create_processing_report(chunks, collection_name)
    
    def create_processing_report(self, chunks: List[Dict], collection_name: str):
        """Create a processing summary report"""
        report = {
            'total_chunks': len(chunks),
            'collection_name': collection_name,
            'sections': {},
            'content_types': {},
            'avg_chunk_size': sum(c['metadata']['char_count'] for c in chunks) / len(chunks),
            'top_keywords': []
        }
        
        # Analyze sections
        for chunk in chunks:
            section = chunk['metadata']['section']
            if section not in report['sections']:
                report['sections'][section] = 0
            report['sections'][section] += 1
            
            content_type = chunk['metadata']['content_type']
            if content_type not in report['content_types']:
                report['content_types'][content_type] = 0
            report['content_types'][content_type] += 1
        
        # Save report
        with open('processing_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Processing Report:")
        print(f"   Total chunks: {report['total_chunks']}")
        print(f"   Average chunk size: {report['avg_chunk_size']:.0f} characters")
        print(f"   Number of sections: {len(report['sections'])}")
        print(f"   Content types: {list(report['content_types'].keys())}")


# Main execution
if __name__ == "__main__":
    # Option 1: Use HuggingFace model (recommended for technical docs - FREE and runs locally)
    processor = DocumentationProcessor(
        embedding_model='sentence-transformers/all-mpnet-base-v2'
        # Alternative models:
        # 'BAAI/bge-large-en-v1.5'  # Better quality, larger model
        # 'sentence-transformers/all-MiniLM-L6-v2'  # Faster, smaller
    )
    
    # Option 2: Use OpenAI embeddings (requires API key and costs money)
    # import os
    # os.environ['OPENAI_API_KEY'] = 'your-key-here'
    # processor = DocumentationProcessor(embedding_model='openai')
    
    # Process the documentation
    processor.process_and_store(
        file_path='dialogflow_cx_documentation.md',
        collection_name='dialogflow_cx_docs'
    )
