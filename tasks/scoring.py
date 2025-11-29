from datetime import date, datetime

# I just used simple strings for strategy
STRATEGY_SMART = "smart_balance"
STRATEGY_FAST = "fastest_wins"
STRATEGY_IMPACT = "high_impact"
STRATEGY_DEADLINE = "deadline_driven"


def parse_due_date(due_date_str):
    if not due_date_str:
        return None
    try:
        # YYYY-MM-DD
        return datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def build_dependents_map(tasks):
    dependents_map = {}
    for task in tasks:
        task_id = task.id or task.title
        deps = task.dependencies or []
        for dep in deps:
            dependents_map[dep] = dependents_map.get(dep, 0) + 1
    return dependents_map


def score_task(task, dependents_map, strategy=STRATEGY_SMART):

    today = date.today()
    raw_due_date = task.get("due_date") or None
    due_date = parse_due_date(raw_due_date)

    importance = task.get("importance") or 5
    try:
        importance = int(importance)
    except Exception:
        importance = 5
    if importance < 1:
        importance = 1
    if importance > 10:
        importance = 10
    
    hours = task.get("estimated_hours") or 1.0
    try:
        hours = float(hours)
    except Exception:
        hours = 1.0
    if hours <= 0:
        hours = 0.5
    
    task_id = task.get("id") or task.get("title")
    dependents = dependents_map.get(task_id, 0)

    score = 0
    explanation_parts = []

    # urgency
    if due_date:
        days_left = (due_date - today).days
        if days_left <= 0:
            score += 50 + abs(days_left)
            explanation_parts.append(f"Overdue by {abs(days_left)} days.")
        elif days_left == 0:
            score += 40
            explanation_parts.append("Due today.")
        elif days_left <= 3:
            score += 30
            explanation_parts.append(f"Due in {days_left} days.")
        elif days_left <= 7:
            score += 15
            explanation_parts.append(f"Due in {days_left} days.")
        else:
            score += 5
            explanation_parts.append(f"Due in {days_left} days.")
    else:
        explanation_parts.append("No due date.")

    
    # importance
    score += importance * 5
    explanation_parts.append(f"Importance: {importance}/10.")

    # effort
    if hours <= 2:
        score += 10
        explanation_parts.append("Low effort.")
    elif hours <= 4:
        score += 5
        explanation_parts.append("Medium effort.")
    else:
        score += 0
        explanation_parts.append("High effort.")
    

    # dependents
    if dependents > 0:
        score += dependents * 5
        explanation_parts.append(f"Dependents: {dependents}.")
    

    # strategy
    if strategy == STRATEGY_FAST:
        if hours <= 2:
            score += 20
            explanation_parts.append("Fastest wins strategy.")
        score -= importance # because we want to prioritize quick time
    elif strategy == STRATEGY_IMPACT:
        score += importance * 5
        explanation_parts.append("High impact strategy.")
    elif strategy == STRATEGY_DEADLINE:
        if due_date:
            score += 20
            explanation_parts.append("Deadline driven strategy.")
    else:
        # default
        explanation_parts.append("Smart balance strategy.")

    # priorty level
    if score >= 100:
        level = "High"
    elif score >= 60:
        level = "Medium"
    else:
        level = "Low"
    
    explanation = " ".join(explanation_parts)

    return {
        "task": task,
        "score": score,
        "priority_level": level,
        "explanation": explanation
    }


def analyze_tasks(tasks, strategy=STRATEGY_SMART):

    dependents_map = build_dependents_map(tasks)

    scored = []
    for task in tasks:
        scored_task = score_task(task, dependents_map, strategy)
        scored.append(scored_task)
    
    scored.sort(key=lambda x: x["score"], reverse=True)

    return {
        "strategy": strategy,
        "tasks": scored,
    }

  
