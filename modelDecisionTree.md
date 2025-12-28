# 🔮 GitHub Copilot Model Selection Cheat Sheet

A simple, reliable guide for choosing the right model inside **GitHub Copilot** (Chat, Inline, or Agents).
---

### Disclaimer
Model availability depends on your Copilot plan and org settings.

---
```mermaid
flowchart TB
    Start["Start"] --> NeedFast["Need speed & low cost?"]

    NeedFast -- Yes --> FastModels["Fast models"]
    NeedFast -- No --> GeneralCoding["Everyday coding task?"]

    GeneralCoding -- Yes --> BalancedModels["Balanced models"]
    GeneralCoding -- No --> DeepReasoning["Hard problem or deep reasoning?"]

    DeepReasoning -- Yes --> DeepModels["Deep-reasoning models"]
    DeepReasoning -- No --> CodeFocus["Large or strict code generation?"]

    CodeFocus -- Yes --> CodeModels["Code-focused models"]
    CodeFocus -- No --> AgentWorkflows["Using agents or tools?"]

    AgentWorkflows -- Yes --> AgentModels["Agent-strong models"]
    AgentWorkflows -- No --> BalancedModels

    FastModels --> Done["Done"]
    BalancedModels --> Done
    DeepModels --> Done
    CodeModels --> Done
    AgentModels --> Done

    FastModels:::Peach
    DeepModels:::Sky
    CodeModels:::Rose
    AgentModels:::Aqua
    BalancedModels:::Pine

    classDef Peach stroke-width:1px, stroke:#FBB35A, fill:#FFEFDB, color:#8F632D
    classDef Rose stroke-width:1px, stroke:#FF5978, fill:#FFDFE5, color:#8E2236
    classDef Aqua stroke-width:1px, stroke:#46EDC8, fill:#DEFFF8, color:#378E7A
    classDef Sky stroke-width:1px, stroke:#374D7C, fill:#E2EBFF, color:#374D7C
    classDef Pine stroke-width:1px, stroke:#254336, fill:#27654A, color:#FFFFFF
```
---

## 🧭 Decision Flow

### 1️⃣ Do you need maximum speed and lowest cost?
➡️ **Use FAST models**

**Models**
- GPT-5 mini  
- Claude Haiku 4.5  
- Gemini Flash  

**Use when**
- You want quick answers
- You're summarizing, drafting, or doing simple refactors
- Low cost matters for large volumes of prompts

---

### 2️⃣ Do you need general, everyday coding assistance?
➡️ **Use BALANCED models**

**Models**
- GPT-4.1  
- Claude Sonnet 4 / 4.5  
- Gemini Pro  

**Use when**
- Writing code
- Debugging normal issues
- Explaining code
- Typical daily work

---

### 3️⃣ Are you dealing with a hard problem requiring deep reasoning?
➡️ **Use DEEP-REASONING models**

**Models**
- GPT-5 / 5.1 / 5.2  
- Claude Opus 4.5  
- Gemini 2.5 Pro  

**Use when**
- Multi-file reasoning
- Architecture-level analysis
- Tough bugs
- Complex logic or multi-step problems

---

### 4️⃣ Is the task code-first or code-heavy?
(refactoring, translating, generating large code blocks)

➡️ **Use CODE-FOCUSED models**

**Models**
- GPT-5 Codex  
- GPT-5.1 Codex  
- Codex Mini (preview)  

**Use when**
- Strict, deterministic code generation
- Large refactors
- Code migration across languages

---

### 5️⃣ Do you need multi-file edits, tools, or agent workflows?
➡️ **Use AGENT-STRONG models**

**Models**
- Claude Sonnet 4.5  
- GPT-4.1  
- GPT-5 series (if enabled)  

**Use when**
- Using GitHub Copilot Agents
- Multi-file refactoring
- Tool-based modifications
- Complex workflows

---

## 🗂️ Model Family Overview

| Category        | Best For                          | Models |
|-----------------|----------------------------------|--------|
| **FAST**        | Speed + low cost                 | GPT-5 mini, Claude Haiku 4.5, Gemini Flash |
| **BALANCED**    | Daily coding                     | GPT-4.1, Claude Sonnet 4 / 4.5, Gemini Pro |
| **DEEP-REASONING** | Complex problem solving     | GPT-5.x, Claude Opus 4.5, Gemini 2.5 Pro |
| **CODE-FOCUSED** | Deterministic, strict code     | GPT-5 Codex, GPT-5.1 Codex, Codex Mini |
| **AGENT-STRONG** | Multi-file, tool use, agents    | Claude Sonnet 4.5, GPT-4.1, GPT-5 |

---

## 🎯 Quick Recommendations

- **Most users, most of the time:** Claude Sonnet 4.5 or GPT-4.1  
- **Hard problems:** Claude Opus 4.5 or GPT-5.x  
- **Fast & cheap:** GPT-5 mini  
- **Strict coding:** GPT-5 Codex  
- **Agent workflows:** Claude Sonnet 4.5 or GPT-5  
