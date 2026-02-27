# Skills Library

Central repository of skills for building projects with Claude Code.

## How to Use

### Slash Commands (Global - work in ANY project)
Type directly in Claude Code:
```
/smart-debug         → דיבאג חכם עם sub-agents
/code-review         → סקירת קוד מקיפה
/security-audit      → סריקת אבטחה
/write-tests         → כתיבת טסטים
/refactor-clean      → ניקוי וריפקטורינג
/doc-generate        → יצירת תיעוד
/ultra-think         → חשיבה עמוקה על בעיה
... ועוד 49 פקודות
```

### Library Skills (Knowledge/Patterns)
```
/skill web-app/react-vite      → טען פטרנים לבניית React app
/skill api/fastapi             → טען פטרנים לבניית FastAPI
/skill ai-agent/claude-agent   → טען פטרנים לבניית AI agent
```

---

## Slash Commands (56 סקילים זמינים)

### Debugging & Error Analysis
| Command | Description | Source |
|---------|-------------|--------|
| `/smart-debug` | דיבאג חכם עם sub-agents מיוחדים | wshobson |
| `/debug-error` | ניתוח שגיאות ספציפיות | qdhenry |
| `/debug-trace` | מעקב אחר flow של בעיה | wshobson |
| `/error-analysis` | ניתוח סיבת השורש של שגיאות | wshobson |
| `/fix-issue` | תיקון Issue ספציפי | qdhenry |

### Code Quality & Refactoring
| Command | Description | Source |
|---------|-------------|--------|
| `/code-review` | סקירת קוד מלאה | qdhenry |
| `/refactor-clean` | ניקוי קוד + SOLID principles | wshobson |
| `/code-explain` | הסבר קוד מורכב | wshobson |
| `/code-migrate` | מיגרציה לטכנולוגיה חדשה | wshobson |
| `/tech-debt` | זיהוי וטיפול בחוב טכני | wshobson |
| `/quality` | בדיקת איכות כוללת | angakh |
| `/clean` | ניקוי קוד ישן | angakh |

### Testing
| Command | Description | Source |
|---------|-------------|--------|
| `/write-tests` | כתיבת טסטים לקוד קיים | qdhenry |
| `/test-coverage` | ניתוח coverage + מילוי פערים | qdhenry |
| `/generate-test-cases` | יצירת test cases מקיפים | qdhenry |
| `/e2e-setup` | הגדרת E2E testing | qdhenry |
| `/tdd-red` | TDD שלב 1 - כתיבת טסטים נכשלים | wshobson |
| `/tdd-green` | TDD שלב 2 - קוד שמעביר טסטים | wshobson |
| `/tdd-refactor` | TDD שלב 3 - ריפקטורינג בטוח | wshobson |
| `/test` | הרצת טסטים | angakh |
| `/verify` | אימות שהכל עובד | angakh |

### Security
| Command | Description | Source |
|---------|-------------|--------|
| `/security-audit` | סריקת אבטחה מקיפה | qdhenry |
| `/security-hardening` | חיזוק האבטחה | qdhenry |
| `/security-scan` | סריקה מהירה לפגיעויות | wshobson |
| `/dependency-audit` | בדיקת dependencies לאבטחה | qdhenry |
| `/deps-audit` | סריקת תלויות | wshobson |

### Documentation
| Command | Description | Source |
|---------|-------------|--------|
| `/doc-generate` | יצירת תיעוד אוטומטי | wshobson |
| `/generate-api-documentation` | תיעוד API מלא | qdhenry |
| `/create-architecture-documentation` | תיעוד ארכיטקטורה | qdhenry |
| `/migration-guide` | מדריך מיגרציה | qdhenry |
| `/troubleshooting-guide` | מדריך פתרון בעיות | qdhenry |
| `/update-docs` | עדכון תיעוד קיים | angakh |

### Performance
| Command | Description | Source |
|---------|-------------|--------|
| `/performance-audit` | ניתוח performance מקיף | qdhenry |
| `/optimize-database-performance` | אופטימיזציית DB | qdhenry |
| `/implement-caching-strategy` | הוספת caching | qdhenry |
| `/optimize-bundle-size` | קטנת bundle | qdhenry |
| `/cost-optimize` | אופטימיזציית עלויות | wshobson |

### Git & Workflow
| Command | Description | Source |
|---------|-------------|--------|
| `/commit` | יצירת commit מוסבר | angakh |
| `/pr-create` | יצירת Pull Request | angakh |
| `/pr-enhance` | שיפור PR קיים | wshobson |
| `/deploy-checklist` | צ'קליסט לפני deploy | wshobson |
| `/context-save` | שמירת context לסשן הבא | wshobson |
| `/context-restore` | שחזור context | wshobson |

### API & Architecture
| Command | Description | Source |
|---------|-------------|--------|
| `/api-scaffold` | יצירת scaffold לAPI | wshobson |
| `/scaffold` | יצירת skeleton לפרויקט | angakh |
| `/architecture-scenario-explorer` | ניתוח תרחישים ארכיטקטוניים | qdhenry |
| `/incremental-feature-build` | בניית feature בשלבים | qdhenry |
| `/ultra-think` | חשיבה עמוקה ומסודרת | qdhenry |

### Project Management
| Command | Description | Source |
|---------|-------------|--------|
| `/overview` | סקירה כללית של הפרויקט | angakh |
| `/onboard` | הכנסת מפתח חדש לפרויקט | wshobson |
| `/standup-notes` | כתיבת standup notes | wshobson |
| `/multi-agent-review` | סקירה עם מספר agents | wshobson |
| `/deps` | ניהול dependencies | angakh |

### Skills Management (My Own)
| Command | Description |
|---------|-------------|
| `/skill <cat>/<name>` | טען skill מהספרייה |
| `/list-skills` | הצג כל הsqills הזמינים |
| `/new-skill <cat>/<name>` | צור skill חדש |

---

## Library Skills (Knowledge Base)

Files in `library/` contain patterns, conventions, and best practices:

### Web App (`library/web-app/`)
| Skill | Description |
|-------|-------------|
| `react-vite` | React 18 + Vite + TypeScript + Tailwind |

### API (`library/api/`)
| Skill | Description |
|-------|-------------|
| `fastapi` | Python FastAPI + SQLAlchemy + PostgreSQL |
| `api-design-principles` | REST API design best practices |

### Database (`library/database/`)
| Skill | Description |
|-------|-------------|
| `postgres-setup` | PostgreSQL setup, Docker, migrations |
| `database-architect` | Database architecture patterns |
| `postgres-best-practices` | PostgreSQL performance and best practices |

### AI Agent (`library/ai-agent/`)
| Skill | Description |
|-------|-------------|
| `claude-agent` | Claude AI agent with tool use |

### Security (`library/security/`)
| Skill | Description |
|-------|-------------|
| `security` | General security practices |
| `auditor` | Security audit methodologies |

### Architecture (`library/architecture/`)
| Skill | Description |
|-------|-------------|
| `software-architecture` | Software architecture principles |
| `patterns` | Architecture patterns reference |

### DevOps (`library/devops/`)
| Skill | Description |
|-------|-------------|
| `docker-compose` | Docker + Compose multi-service apps |

### Design (`library/design/`)
| Skill | Description |
|-------|-------------|
| `design-md` | Semantic design system synthesis for Stitch projects |
| `ui-ux-designer` | UI/UX design, design systems, accessibility |
| `web-design-guidelines` | Web interface guidelines compliance review |
| `frontend-design` | Production-grade frontend interfaces |
| `mobile-design` | Mobile-first design for iOS and Android |
| `canvas-design` | Visual art creation with design philosophy |
| `tailwind-design-system` | Tailwind CSS design system |
| `design-orchestration` | Design orchestration skills |

### Code (`library/code/`)
| Skill | Description |
|-------|-------------|
| `clean-code` | Clean code principles and best practices |
| `code-review-excellence` | Comprehensive code review |
| `refactor-clean` | Code refactoring and cleanup |
| `frontend-dev-guidelines` | Frontend development patterns |
| `backend-dev-guidelines` | Backend development patterns |
| `test-driven-development` | TDD methodology |
| `doc-generate` | Automatic documentation generation |
| `langchain-agent` | LangChain agent development |
| `autonomous-agents` | Autonomous agent patterns |
| `ai-agents-architect` | AI agents architecture |

---

## Sources
- [wshobson/commands](https://github.com/wshobson/commands) - Production-ready slash commands
- [qdhenry/Claude-Command-Suite](https://github.com/qdhenry/Claude-Command-Suite) - Comprehensive command suite
- [angakh/claude-skills-starter](https://github.com/angakh/claude-skills-starter) - Essential starter skills
