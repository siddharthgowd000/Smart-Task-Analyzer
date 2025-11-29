from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .scoring import analyze_tasks, STRATEGY_SMART, STRATEGY_FAST, STRATEGY_IMPACT, STRATEGY_DEADLINE
from .models import Task


def bad_request(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)


@csrf_exempt
@require_http_methods(["POST"])
def analyze_view(request):
    try:
        data = json.loads(request.body)
        tasks = data.get("tasks", [])
        strategy = data.get("strategy", STRATEGY_SMART)
        if not isinstance(tasks, list):
            return bad_request("Tasks must be a list")
        if strategy not in [STRATEGY_SMART, STRATEGY_FAST, STRATEGY_IMPACT, STRATEGY_DEADLINE]:
            return bad_request("Invalid strategy")
        result = analyze_tasks(tasks, strategy)
        return JsonResponse({"success": True, "result": result})
    except Exception as e:
        return bad_request(str(e))


@require_http_methods(["GET"])
def suggest_view(request):
    
    try:
        strategy = request.GET.get("strategy", STRATEGY_SMART)
        if strategy not in [STRATEGY_SMART, STRATEGY_FAST, STRATEGY_IMPACT, STRATEGY_DEADLINE]:
            strategy = STRATEGY_SMART
        
        tasks = []
        for task in Task.objects.all():
            tasks.append({
                "id": task.id,
                "title": task.title,
                "due_date": task.due_date,
                "estimated_hours": task.estimated_hours,
                "importance": task.importance,
                "dependencies": task.dependencies,
            })

        result = analyze_tasks(tasks, strategy)
        top3 = result["tasks"][:3]
       

        return JsonResponse({
            "success": True,
            "strategy": strategy,
            "today": str(date.today()),
            "suggested_tasks": top3,
        })