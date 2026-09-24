const list = document.querySelector("#todos");
const summary = document.querySelector("#summary");
const form = document.querySelector("#todo-form");
const input = document.querySelector("#title");

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.status === 204 ? null : response.json();
}

async function render() {
  const [todos, stats] = await Promise.all([
    request("/api/todos"),
    request("/stats"),
  ]);
  summary.textContent = `共 ${stats.total} 項，尚有 ${stats.pending} 項未完成`;
  list.replaceChildren(...todos.map((todo) => {
    const item = document.createElement("li");
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = todo.completed;
    checkbox.addEventListener("change", async () => {
      await request(`/api/todos/${todo.id}`, {
        method: "PATCH",
        body: JSON.stringify({ completed: checkbox.checked }),
      });
      await render();
    });
    label.append(checkbox, document.createTextNode(todo.title));
    if (todo.completed) label.classList.add("completed");
    const remove = document.createElement("button");
    remove.textContent = "刪除";
    remove.addEventListener("click", async () => {
      await request(`/api/todos/${todo.id}`, { method: "DELETE" });
      await render();
    });
    item.append(label, remove);
    return item;
  }));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await request("/api/todos", {
    method: "POST",
    body: JSON.stringify({ title: input.value.trim() }),
  });
  form.reset();
  await render();
});

render().catch(() => { summary.textContent = "無法載入資料"; });

