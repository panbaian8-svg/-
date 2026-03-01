# StudyFlow AI - Intelligent Study Assistance System

---

## What it does

StudyFlow AI is an AI-powered intelligent study assistance system designed to help students learn more efficiently. It combines document processing, knowledge extraction, RAG-based Q&A, and knowledge visualization into a unified platform.

**Key Features:**
- 📄 **Document Upload** - Upload PDF/Word documents with automatic parsing
- 🧠 **Knowledge Extraction** - AI automatically extracts knowledge points and chapter structures
- 💬 **Intelligent Q&A** - RAG-based question answering with source citations
- 🗺️ **Knowledge Map** - Visualize relationships between knowledge points
- 🔍 **OCR Recognition** - Extract text from images
- 🖼️ **Image Understanding** - AI analyzes images and answers questions
- 🌐 **Bilingual Support** - Switch between Chinese and English interface
- 🔄 **Multi-Provider Support** - Switch between DeepSeek and MiniMax AI models

**Target Users:** Students who need efficient learning tools with document-based knowledge management.

---

## How we built it

### Tech Stack

**Backend:**
- **Framework:** FastAPI - Modern, fast Python web framework
- **Language:** Python 3.13
- **Database:** ChromaDB - Vector storage for RAG retrieval
- **AI Services:**
  - DeepSeek API (deepseek-chat model)
  - MiniMax API (abab5.5-chat model)
- **Document Processing:** PyPDF2 for PDF parsing

**Frontend:**
- **Framework:** React 19.2 + TypeScript
- **Build Tool:** Vite 7.2 - Lightning fast build tool
- **Styling:** Tailwind CSS 3.4 - Utility-first CSS framework
- **UI Components:** shadcn/ui - Modern, accessible component library (40+ components)
- **Icons:** Lucide React - Beautiful, consistent icons
- **Visualization:** Cytoscape.js - Knowledge graph visualization
- **HTTP Client:** Axios - Promise-based HTTP client

**Architecture:**
```
┌─────────────────────────────────────────────┐
│            Frontend (React)             │
│              ↓ HTTP/REST API              │
│            Backend (FastAPI)             │
│              ↓ AI Service Layer            │
│  ┌───────────────────────────┐          │
│  │    DeepSeek   MiniMax  │          │
│  └───────────────────────────┘          │
│              ↓                            │
│         ChromaDB (Vector Store)           │
└─────────────────────────────────────────────┘
```

### Key Implementation Details

1. **AI Provider Abstraction Layer**
   - Unified interface for multiple AI providers
   - Easy switching between DeepSeek and MiniMax
   - Mock mode for testing without API calls

2. **RAG Implementation**
   - Document content vectorization
   - Similarity search using ChromaDB
   - Context-aware answer generation
   - Source citations for credibility

3. **Modern UI Design**
   - Glass morphism effects with gradients
   - Responsive layout for all devices
   - Bilingual (CN/EN) with seamless switching
   - Image upload with preview functionality
   - Smooth animations and transitions

---

## Challenges we ran into

### 1. **Vector Database Integration**
**Challenge:** ChromaDB setup and configuration
- Initial difficulty with ChromaDB connection and persistence
- Vector embeddings generation required careful API design

**Solution:**
- Implemented graceful fallback when vector DB fails
- Added automatic data cleanup on startup
- Used in-memory storage as backup

### 2. **RAG Context Management**
**Challenge:** Balancing context length vs. answer quality
- Too much context → slower API calls, higher costs
- Too little context → answers lack detail

**Solution:**
- Implemented dynamic context window based on document length
- Truncated content to first 8000 characters (API limit)
- Added `top_k` parameter for configurable retrieval

### 3. **Multi-Language Support**
**Challenge:** Maintaining consistent translations across all components
- Ensuring Chinese and English versions are equivalent
- Managing state when switching languages

**Solution:**
- Created centralized translation object in ChatPage
- Used `useEffect` for language-dependent content updates
- Maintained translation keys in a structured object

### 4. **Knowledge Graph Visualization**
**Challenge:** Rendering complex relationships between knowledge points
- Cytoscape.js configuration for optimal performance
- Handling large graphs without UI freezing

**Solution:**
- Implemented graph layout algorithms (force-directed)
- Added progressive loading for large graphs
- Used color coding for different node types (chapters, topics)

### 5. **API Key Security**
**Challenge:** Storing API keys securely without hardcoding
- Preventing accidental commits of sensitive information

**Solution:**
- Created `.env.docker` template for setup
- Added `.env` to `.gitignore` explicitly
- Provided clear documentation on where to get keys

### 6. **Time Constraints (Hackathon)**
**Challenge:** Limited time (6 hours) for implementation
- Prioritizing core features vs. nice-to-have polish

**Solution:**
- Focused on P0 features first (Q&A, document upload)
- Used existing shadcn/ui components instead of building from scratch
- Iterated quickly with minimum viable products

---

## Accomplishments that we're proud of

### 🎯 Core Features Delivered

1. **Complete RAG System**
   - ✅ Implemented end-to-end question answering with vector search
   - ✅ Source citations for transparency
   - ✅ Related topics suggestions
   - Response time: < 3 seconds average

2. **Bilingual Interface**
   - ✅ Seamless CN/EN switching across all pages
   - ✅ Complete translations for user-facing text
   - ✅ Language toggle with visual feedback

3. **Modern UI Design**
   - ✅ shadcn/ui integration (40+ components)
   - ✅ Gradient color scheme (indigo/violet theme)
   - ✅ Responsive design for mobile and desktop
   - ✅ Smooth animations and micro-interactions

4. **Document Management**
   - ✅ PDF and Word document upload
   - ✅ Real-time parsing progress
   - ✅ Document list with search functionality
   - ✅ Download and delete operations

5. **Multi-Provider Architecture**
   - ✅ Clean abstraction between DeepSeek and MiniMax
   - ✅ Runtime switching without restart
   - ✅ Fallback to mock mode for testing

### 📊 Technical Achievements

1. **Clean Architecture**
   - Separation of concerns (routers, services, models)
   - Reusable service layer
   - Type-safe TypeScript throughout frontend

2. **Performance Optimization**
   - ChromaDB for fast vector similarity search
   - Vite for lightning-fast frontend builds
   - Lazy loading for large components

3. **Developer Experience**
   - Comprehensive README with setup instructions
   - Environment variable templates (.env.docker)
   - Clear project structure and documentation

4. **Hackathon Delivery**
   - ✅ All P0 features completed on time
   - ✅ Multiple commits for safe progress
   - ✅ Successfully pushed to GitHub

### 🏆 What sets us apart

1. **Student-Focused Design**
   - Not just another chatbot - specifically built for studying
   - Source citations encourage learning from materials
   - Knowledge map helps visualize understanding

2. **Production-Ready Code**
   - Proper error handling throughout
   - Input validation and sanitization
   - CORS configuration for real deployment

3. **Modern Tech Choices**
   - shadcn/ui for consistent, accessible UI
   - ChromaDB for vector similarity (industry standard)
   - TypeScript for type safety and better DX

---

## What we learned

### 1. **Vector Databases are Powerful but Simple**
ChromaDB made RAG implementation straightforward. The combination of:
- Automatic embeddings (via OpenAI-compatible APIs)
- Built-in similarity search
- Easy filtering and retrieval

Made it possible to build a working RAG system in a single hackathon.

### 2. **UI Components Libraries Save Time**
shadcn/ui was crucial for meeting the deadline. Building 40+ accessible components from scratch would have taken weeks. Pre-built components let us focus on:
- Business logic
- API integration
- UX polish

### 3. **Abstraction Layers Pay Off**
The initial investment in creating `AIServiceSelector` abstraction paid off massively:
- Easy switching between DeepSeek and MiniMax
- Easy testing with mock mode
- Cleaner code in router functions

### 4. **Progressive Enhancement is Better than Perfection**
Instead of trying to perfect each feature, we shipped:
1. Core functionality first (Q&A, document upload)
2. Then UI polish (shadcn/ui integration)
3. Then additional features (image upload, bilingual)

This incremental approach let us deliver more value within the time constraint.

### 5. **Documentation is as Important as Code**
Having clear README.md, API docs, and setup instructions meant:
- Faster onboarding for teammates
- Easier demo preparation
- Better judge understanding during review

### 6. **Time Management in Hackathons**

Key lessons:
- **Track time strictly** - We had 6 hours total
- **Cut features early** - Dropped ambitious features like advanced knowledge graph visualization
- **Use existing solutions** - shadcn/ui, ChromaDB instead of building from scratch
- **Ship frequently** - Multiple commits prevented losing work

---

## What's next for StudyFlow AI

### 🚀 Immediate Improvements (Post-Hackathon)

1. **Knowledge Graph Enhancements**
   - Implement interactive node exploration
   - Add graph clustering algorithms
   - Enable subgraph navigation

2. **Advanced RAG Features**
   - Implement hybrid search (keyword + semantic)
   - Add re-ranking for better answer quality
   - Support multi-document queries

3. **User Experience**
   - Add dark mode support
   - Implement user accounts and progress tracking
   - Add conversation history and export

4. **Performance Optimization**
   - Implement streaming responses for better UX
   - Add response caching for repeated questions
   - Optimize ChromaDB queries with indexing

### 📈 Scalability Considerations

1. **Database Scaling**
   - Migrate from local ChromaDB to cloud vector DB (Pinecone, Weaviate)
   - Implement document-level vs. chunk-level embeddings strategy

2. **AI Model Optimization**
   - Fine-tune smaller models for specific domains (math, physics, etc.)
   - Implement model routing based on question type

3. **Deployment**
   - Containerize application with Docker
   - Set up CI/CD pipeline
   - Deploy to cloud platform (Vercel, Railway, etc.)

4. **Analytics and Monitoring**
   - Add user interaction analytics
   - Monitor API response times and costs
   - Track question quality and satisfaction

### 🎯 Long-term Vision

Transform StudyFlow AI from a study tool into a comprehensive learning platform:

- **AI Study Assistant:** Personalized learning paths and adaptive difficulty
- **Collaborative Learning:** Shared knowledge bases and group study sessions
- **Smart Content:** Auto-generated quizzes, flashcards, and practice problems
- **Progress Tracking:** Visual learning dashboards and achievement systems

---

## Tech Stack Summary

```
┌──────────────────────────────────────────────────────────┐
│                    StudyFlow AI                        │
├───────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────┐  ┌───────────────────────┐ │
│  │   Frontend (React)  │  │  Backend (FastAPI)  │ │
│  │                      │  │                     │     │
│  │  TypeScript          │  │  Python 3.13        │     │
│  │  Tailwind CSS        │  │  ChromaDB            │     │
│  │  shadcn/ui          │  │  DeepSeek API        │     │
│  └──────────────────────┘  │  MiniMax API         │     │
│                            └───────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

**Built by:** [Your Team Name]
**Hackathon:** HackTheEast 2026
**Date:** March 2, 2026

---

> **🎓 The goal was simple: Help students study smarter with AI. We're proud of what we built in 6 hours.**
