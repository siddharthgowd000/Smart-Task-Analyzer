from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .scoring import analyze_tasks, STRATEGY_SMART, STRATEGY_FAST, STRATEGY_IMPACT, STRATEGY_DEADLINE
from .models import Task
from datetime import date


def bad_request(message, status=400):
    response = JsonResponse({"success": False, "message": message}, status=status)
    response["Access-Control-Allow-Origin"] = "*"
    return response


@csrf_exempt
def analyze_view(request):
    # Debug logging
    print(f"analyze_view called - Method: {request.method}, Path: {request.path}")
    
    # Handle OPTIONS for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    # Only allow POST
    if request.method != "POST":
        print(f"Method {request.method} not allowed for analyze_view")
        return JsonResponse({"success": False, "message": f"Method {request.method} not allowed. Only POST is supported."}, status=405)
    
    try:
        # Parse JSON request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return bad_request(f"Invalid JSON: {str(e)}")
        
        tasks = data.get("tasks", [])
        strategy = data.get("strategy", STRATEGY_SMART)
        
        if not isinstance(tasks, list):
            return bad_request("Tasks must be a list")
        
        if not tasks:
            return bad_request("Tasks list cannot be empty")
        
        # Validate strategy
        if strategy not in [STRATEGY_SMART, STRATEGY_FAST, STRATEGY_IMPACT, STRATEGY_DEADLINE]:
            return bad_request(f"Invalid strategy. Must be one of: {STRATEGY_SMART}, {STRATEGY_FAST}, {STRATEGY_IMPACT}, {STRATEGY_DEADLINE}")
        
        # Analyze tasks
        result = analyze_tasks(tasks, strategy)
        response = JsonResponse({"success": True, "result": result})
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
    except json.JSONDecodeError as e:
        return bad_request(f"Invalid JSON in request: {str(e)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return bad_request(f"Server error: {str(e)}")


@csrf_exempt
def suggest_view(request):
    # Handle OPTIONS for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    # Only allow GET
    if request.method != "GET":
        return JsonResponse({"success": False, "message": f"Method {request.method} not allowed. Only GET is supported."}, status=405)
    
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
       

        response = JsonResponse({
            "success": True,
            "strategy": strategy,
            "today": str(date.today()),
            "suggested_tasks": top3,
        })
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    except Exception as e:
        return bad_request(str(e))