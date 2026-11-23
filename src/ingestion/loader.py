from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from docx import Document as DocxDocument

SUPPORTED_FILE_TYPES = {".pdf", ".txt", ".md", ".docx"}

def load_file(file_path: Path) -> list[Document]:
    """
    Load a file and return a list of Document objects.
    """
    suffix = file_path.suffix.lower()
    
    if suffix == ".pdf":
        return PyPDFLoader(str(file_path)).load()
    
    if suffix in {".txt", ".md"}:
        return TextLoader(str(file_path), encoding="utf-8").load()
    
    if suffix == ".docx":
        doc =  DocxDocument(str(file_path))
        text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
        return [Document(page_content=text, metadata={"source": str(file_path)})]
    
    raise ValueError(f"Unsupported file type: {suffix}. Supported types are: {SUPPORTED_FILE_TYPES}")