# AdaptIQ

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vue.js)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch)
![Neo4j](https://img.shields.io/badge/Neo4j-graph%20db-008CC1?logo=neo4j)
![CI](https://github.com/kalekakenqq/adaptiq/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-70%25%2B-brightgreen)

**AdaptIQ** — мультимодальная адаптивная образовательная платформа с искусственным интеллектом.

## Описание проекта и научная новизна

AdaptIQ объединяет в единой архитектуре шесть взаимосвязанных AI-модулей, обеспечивающих
адаптацию образовательного процесса к когнитивному и эмоциональному состоянию обучающегося
в реальном времени. Научная новизна работы заключается в мультимодальном слиянии
(multimodal fusion) сигналов компьютерного зрения, обработки естественного языка и
поведенческих метрик в единый индекс когнитивной нагрузки, на основе которого
обучаемый с подкреплением (RL) агент принимает решения об адаптации учебного материала,
а слой объяснимого искусственного интеллекта (XAI) делает эти решения интерпретируемыми
для преподавателя и студента.

## Архитектура

```mermaid
flowchart TB
    subgraph Client["Frontend (Vue.js 3)"]
        UI[Student / Teacher UI]
        Cam[Camera Stream]
    end

    subgraph Backend["Backend (FastAPI)"]
        WS[WebSocket Gateway]
        API[REST API]
        Engine[Adaptive Engine]
    end

    subgraph AI["AI-модули"]
        KG[1. Knowledge Graph - Neo4j]
        CV[2. CV модуль - эмоции / концентрация / eye tracking]
        NLP[3. NLP модуль - RuBERT оценка ответов]
        RL[4. RL агент - PPO]
        AN[5. Предиктивная аналитика - LSTM / clustering]
        XAI[6. XAI слой - SHAP / LIME / Grad-CAM]
    end

    subgraph Storage["Хранилища"]
        PG[(PostgreSQL)]
        NEO[(Neo4j)]
        RED[(Redis)]
    end

    UI --> API
    Cam --> WS
    WS --> CV
    API --> Engine
    Engine --> KG
    Engine --> RL
    Engine --> AN
    NLP --> Engine
    CV --> Engine
    Engine --> XAI
    XAI --> UI
    API --> PG
    KG --> NEO
    Engine --> RED
```

## AI-модули и методы

1. **Knowledge Graph (Neo4j)** — граф знаний предметной области, связи между концепциями и уроками
2. **CV модуль**:
   - CNN на базе EfficientNet-B0 (transfer learning) — классификация эмоций
   - MediaPipe Face Mesh — отслеживание взгляда (eye tracking)
   - Поведенческий анализ концентрации внимания
   - Grad-CAM — визуализация внимания CNN
3. **NLP модуль**:
   - RuBERT (fine-tuned) — оценка качества открытых текстовых ответов
   - sentence-transformers — семантическое сравнение ответов с эталоном
   - Attention visualization — визуализация весов внимания трансформера
4. **RL агент**:
   - PPO (Proximal Policy Optimization, Stable-Baselines3) — выбор следующего учебного материала
   - Кастомный Gym environment, моделирующий обучающуюся сессию
   - Reward shaping на основе прогресса и когнитивной нагрузки
5. **Предиктивная аналитика**:
   - LSTM — предсказание результата экзамена по динамике сессий
   - K-Means + UMAP — кластеризация студентов по поведенческим паттернам
   - Autoencoder — детекция аномального поведения
   - IRT (Item Response Theory) — оценка сложности вопросов и способностей студента
6. **XAI слой**:
   - SHAP — атрибуция признаков для табличных моделей
   - LIME — локальные интерпретируемые объяснения
   - Grad-CAM — визуализация значимых областей изображения
   - Attention Visualization — визуализация внимания NLP-модели

## Стек технологий

| Слой | Технологии |
|---|---|
| Backend | FastAPI, Python 3.11, SQLAlchemy, Pydantic |
| ML/DL | PyTorch, HuggingFace Transformers, Stable-Baselines3, scikit-learn |
| CV | MediaPipe, OpenCV, EfficientNet-B0 |
| NLP | RuBERT, sentence-transformers |
| Frontend | Vue.js 3, Vite, Pinia, Chart.js, D3.js |
| Базы данных | PostgreSQL, Neo4j, Redis |
| Очереди задач | Celery |
| Реалтайм | FastAPI WebSocket |
| Деплой | Docker, Docker Compose, Amvera |
| CI/CD | GitHub Actions |

## Инструкция запуска

```bash
cp .env.example .env
docker-compose up --build
```

Backend будет доступен на `http://localhost:8000`, frontend — на `http://localhost:5173`.

## Структура проекта

```
adaptiq/
├── backend/        # FastAPI приложение, ML-модули, тесты
├── frontend/        # Vue.js 3 SPA
├── ml_training/      # скрипты обучения моделей
├── .github/workflows/   # CI/CD пайплайны
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints (основные)

| Метод | Путь | Описание |
|---|---|---|
| POST | `/api/auth/register` | регистрация пользователя |
| POST | `/api/auth/login` | вход и получение JWT |
| GET | `/api/courses` | список курсов |
| GET | `/api/lessons/{id}` | получение урока |
| POST | `/api/sessions/{id}/answer` | отправка ответа на вопрос |
| GET | `/api/analytics/risk/{student_id}` | риск-оценка студента |
| WS | `/ws/session/{id}` | стрим CV-аналитики в реальном времени |

## Скриншоты

_Будут добавлены по мере разработки интерфейса._
