# User Manual & Features Guide - Mohith AI Assistant

Welcome to the **Mohith AI Assistant** workspace. This guide outlines how to use the dashboard, understand features, configure prompt engineering styles, and manage your history and logs.

---

## 🧭 Dashboard Interface Navigation

The sidebar menu navigates you through the workspace features:

1. **Home**: The portal overview showcasing all features, active modules, and quick launching options.
2. **Chat**: The core playground containing conversational bubbles, model parameters selection, streaming outputs, feedback triggers, and response action buttons (Copy, Download, Regenerate).
3. **Prompt Library**: A reference manual displaying the precise System Prompt blueprints and formatting equations used to engineer the completions.
4. **History**: A session history browser enabling you to inspect or restore previous chats to your active workspace.
5. **Feedback**: A lightweight business analytics dashboard listing logs from `feedback.csv` and showing overall helpfulness metric ratios.
6. **Settings**: Configuration center for OpenAI credentials, temperature randomness sliders, and model selectors.
7. **About**: Technical build details and framework information.

---

## 🧠 Understanding Prompt Engineering Styles

Each specialized tool has three built-in Prompt Engineering Styles:

| Style | Tone & Depth | Length Range | Best Used For |
| :--- | :--- | :--- | :--- |
| **Concise** | Direct, highly focused, summary bullet lists, zero preambles. | 50 - 150 words | Rapid answers, quick rewriting, mobile screens. |
| **Medium** | Balanced context, structured overview paragraphs, bullet details. | 200 - 400 words | Email writing, basic definitions, brainstorm lists. |
| **Detailed** | Comprehensive deep-dives, historical facts, checklists, caveats. | 600 - 1000 words | Extended study guides, business model proposals, story chapters. |

---

## 🛠️ Specialized AI Features Reference

### 1. Answer Questions ❓
Ask any query. The system shapes responses from single-sentence truths (Concise) to deep technical breakdowns with historical contexts (Detailed).

### 2. Text Summarizer 📝
- **Concise:** Yields a single, powerful summary statement.
- **Medium:** Provides 3-5 main bullet takeaways.
- **Detailed:** Drafts an executive summary with headers like "Executive Overview" and "Key Themes".

### 3. Business Idea Generator 💡
- **Concise:** Quick value proposition and customer profile snippet.
- **Medium:** Strategic checklist (Value Prop, Revenue Model, Channels).
- **Detailed:** Multi-chapter proposal including execution, GTM plans, risk mitigation, and cost outlines.

### 4. Story Generator 📖
- **Concise:** 100-word flash fiction twists.
- **Medium:** 300-500 word narrative story with clear character motivations.
- **Detailed:** 800-word immersive story with character internal monologues and sensory details.

### 5. Email Writer ✉️
- **Concise:** Action-oriented, 2-3 sentence emails.
- **Medium:** Structured, polite professional email copy.
- **Detailed:** In-depth executive communications, background context, and clear contact guidelines.

### 6. Resume Helper 👔
- **Concise:** Rewrites work descriptions into one impact-driven verb-oriented accomplishment bullet.
- **Medium:** Professional career summary + three accomplishment metrics.
- **Detailed:** Full review, summary rewrite, ATS keyword recommendations, and career bridge checklists.

### 7. Study Assistant 🎓
- **Concise:** Quick dictionary-style definition and one analogy.
- **Medium:** Explanation + core rules + 3 flashcard revision Q&As.
- **Detailed:** Deep lecture breakdown, common student pitfalls, and 5 quiz practice questions with answers.

---

## ⚙️ Optimizing Model Settings

Navigate to **Settings** to adjust completion behaviors:
- **Model**:
  - `gpt-4o-mini` *(Recommended)*: Very fast and cost-efficient for daily use.
  - `gpt-4o`: High reasoning capabilities, ideal for complex business plans or coding challenges.
  - `gpt-3.5-turbo`: Legacy model.
- **Temperature**:
  - `0.0 to 0.3`: Best for accurate factual summaries, Q&As, and resume modifications.
  - `0.7 to 1.0`: Perfect for standard emails and study reviews.
  - `1.2 to 2.0`: Best for creative stories and out-of-the-box business idea generations.
- **Max Generation Tokens**: Restricts the maximum output word count. Set higher values (1500+) for "Detailed" prompt styles.
