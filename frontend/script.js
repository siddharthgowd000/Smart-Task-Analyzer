// API base URL - Django backend runs on port 8000
const API_BASE_URL = "http://127.0.0.1:8000";

let tasks = [];
let nextId = 1;

const taskForm = document.getElementById("taskForm");
const jsonInput = document.getElementById("jsonInput");
const loadJsonBtn = document.getElementById("loadJsonBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const strategySelect = document.getElementById("strategy");
const taskListEl = document.getElementById("taskList");
const statusEl = document.getElementById("status");

taskForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value.trim();
  const due_date = document.getElementById("due_date").value || null;
  const hoursVal = document.getElementById("estimated_hours").value || "1";
  const importanceVal = document.getElementById("importance").value || "5";
  const depsRaw = document.getElementById("dependencies").value.trim();

  if (!title) {
    alert("Title is required");
    return;
  }

  const estimated_hours = parseFloat(hoursVal);
  const importance = parseInt(importanceVal);

  let deps = [];
  if (depsRaw.length > 0) {
    deps = depsRaw
      .split(",")
      .map(function (d) {
        return d.trim();
      })
      .filter(function (d) {
        return d.length > 0;
      });
  }

  const task = {
    id: nextId++,
    title: title,
    due_date: due_date,
    estimated_hours: isNaN(estimated_hours) ? 1 : estimated_hours,
    importance: isNaN(importance) ? 5 : importance,
    dependencies: deps,
  };

  tasks.push(task);
  renderLocalTasks();
  taskForm.reset();
});

loadJsonBtn.addEventListener("click", function () {
  if (!jsonInput.value.trim()) {
    alert("Please paste a JSON array first.");
    return;
  }
  try {
    const parsed = JSON.parse(jsonInput.value.trim());
    if (!Array.isArray(parsed)) {
      alert("JSON must be an array of tasks.");
      return;
    }
    tasks = parsed.map(function (t, index) {
      return {
        id: t.id || t.task_id || index + 1,
        title: t.title || "Task " + (index + 1),
        due_date: t.due_date || null,
        estimated_hours: t.estimated_hours || 1,
        importance: t.importance || 5,
        dependencies: t.dependencies || [],
      };
    });
    nextId = tasks.length + 1;
    renderLocalTasks();
  } catch (err) {
    console.error(err);
    alert("Invalid JSON.");
  }
});

analyzeBtn.addEventListener("click", function () {
  if (tasks.length === 0) {
    alert("Please add at least one task.");
    return;
  }

  statusEl.textContent = "Analyzing...";
  taskListEl.innerHTML = "";

  const payload = {
    strategy: strategySelect.value,
    tasks: tasks,
  };

  // Django backend on port 8000
  fetch(`${API_BASE_URL}/api/tasks/analyze/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then(function (res) {
      return res.text().then(function (text) {
        if (!res.ok) {
          let errorMsg = `HTTP ${res.status} Error`;
          if (text) {
            try {
              const errorData = JSON.parse(text);
              errorMsg = errorData.message || errorMsg;
            } catch (e) {
              errorMsg =
                text.length > 200
                  ? text.substring(0, 200) + "..."
                  : text || errorMsg;
            }
          }
          throw new Error(errorMsg);
        }

        if (!text || text.trim() === "") {
          throw new Error("Empty response from server");
        }

        try {
          return JSON.parse(text);
        } catch (e) {
          console.error("Failed to parse JSON:", text);
          throw new Error("Invalid JSON response from server: " + e.message);
        }
      });
    })
    .then(function (data) {
      if (!data.success) {
        throw new Error(data.message || "Analysis failed");
      }

      // Backend returns: {"success": True, "result": {"strategy": "...", "tasks": [...]}}
      const result = data.result || {};
      const tasksList = result.tasks || [];
      const strategy = result.strategy || strategySelect.value;

      statusEl.textContent = "Strategy: " + strategy;
      renderAnalyzedTasks(tasksList);
    })
    .catch(function (err) {
      console.error("Error details:", err);
      statusEl.textContent = "Failed to analyze.";
      alert(
        err.message ||
          "Failed to analyze tasks. Please check console for details."
      );
    });
});

function renderLocalTasks() {
  taskListEl.innerHTML = "";
  tasks.forEach(function (t) {
    const div = document.createElement("div");
    div.className = "task-card";
    div.innerHTML = `
      <div class="task-header">
        <span>${t.title}</span>
        <span>ID: ${t.id}</span>
      </div>
      <div class="task-meta">
        Due: ${t.due_date || "N/A"} |
        Hours: ${t.estimated_hours} |
        Importance: ${t.importance} |
        Deps: ${
          t.dependencies && t.dependencies.length
            ? t.dependencies.join(", ")
            : "None"
        }
      </div>
    `;
    taskListEl.appendChild(div);
  });
}

function renderAnalyzedTasks(tasksArr) {
  taskListEl.innerHTML = "";

  if (!tasksArr || tasksArr.length === 0) {
    taskListEl.innerHTML =
      "<p style='color: #999; padding: 16px;'>No tasks to display.</p>";
    return;
  }

  tasksArr.forEach(function (t) {
    // Handle nested structure: analyze_tasks returns {task: {...}, score: ..., priority_level: ..., explanation: ...}
    const task = t.task || t;
    const title = task.title || t.title || "Untitled Task";
    const dueDate = task.due_date || t.due_date || null;
    const hours = task.estimated_hours || t.estimated_hours || 0;
    const importance = task.importance || t.importance || 0;
    const dependencies = task.dependencies || t.dependencies || [];
    const score = t.score !== undefined ? t.score : 0;
    const priorityLevel = t.priority_level || "Low";
    const explanation = t.explanation || "No explanation available.";

    const div = document.createElement("div");
    div.className = "task-card priority-" + priorityLevel;
    div.innerHTML = `
      <div class="task-header">
        <span>${title}</span>
        <span>Score: ${score}</span>
      </div>
      <div class="task-meta">
        Priority: ${priorityLevel} |
        Due: ${dueDate || "N/A"} |
        Hours: ${hours} |
        Importance: ${importance} |
        Deps: ${dependencies.length > 0 ? dependencies.join(", ") : "None"}
      </div>
      <div class="explanation">
        ${explanation}
      </div>
    `;
    taskListEl.appendChild(div);
  });
}
