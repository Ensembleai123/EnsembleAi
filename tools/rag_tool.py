
from typing import List, Optional
import pandas as pd
import PyPDF2
import io
from groq import Groq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .tools import Tool

class RAGTool(Tool):
    def __init__(self, file_paths: List[str], chunk_size: int = 1000, chunk_overlap: int = 200):
        self.file_paths = file_paths
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self._initialize_vector_store()

    def _read_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _read_csv(self, file_path: str) -> str:
        df = pd.read_csv(file_path)
        text = ""
        for _, row in df.iterrows():
            text += " | ".join(f"{col}: {row[col]}" for col in df.columns) + "\n"
        return text

    def _initialize_vector_store(self):
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        for file_path in self.file_paths:
            if file_path.lower().endswith('.pdf'):
                text = self._read_pdf(file_path)
            elif file_path.lower().endswith('.csv'):
                text = self._read_csv(file_path)
            else:
                continue

            chunks = text_splitter.split_text(text)
            documents.extend(chunks)

        if documents:
            self.vector_store = FAISS.from_texts(
                documents,
                self.embeddings
            )

    def _generate_answer(self, context, agent):
        insights = agent.model_instance.generate(
            name=agent.name,
            llm=agent.llm,
            work=agent.work,
            role=agent.role,
            context=context
        )
        return insights

    def use(self, agent, n_results: int = 3) -> str:
        if not self.vector_store:
            return "No documents have been processed. Please check the file paths."

        relevant_docs = self.vector_store.similarity_search(agent.work, k=n_results)
        context = "\n".join(doc.page_content for doc in relevant_docs)

        answer = self._generate_answer(context, agent)
        return answer

    def add_document(self, file_path: str):
        if file_path.lower().endswith('.pdf'):
            text = self._read_pdf(file_path)
        elif file_path.lower().endswith('.csv'):
            text = self._read_csv(file_path)
        else:
            return "Unsupported file format. Please provide PDF or CSV files."

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        chunks = text_splitter.split_text(text)
        if self.vector_store:
            self.vector_store.add_texts(chunks)
        else:
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)
