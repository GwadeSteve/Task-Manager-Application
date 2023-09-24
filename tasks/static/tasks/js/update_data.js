function checkForUpdates() {
    fetch('/tasks/api/get_updates/')
        .then(response => response.json())
        .then(data => {
            // Process and display updates in the console or update the UI
            console.log(data.tasks, data.categories);
            updateUI(data);
        })
        .catch(error => {
            console.error('Error fetching updates:', error);
        })
        .finally(() => {
            // Set up the next request after a short delay (e.g., 5 seconds)
            setTimeout(checkForUpdates, 5000);
        });
}

// Start checking for updates
checkForUpdates();
//+237 6557 40501 (Mi)
//+237 6728 67725 (Noela)


//Here i'll get data and update ui accordingly
function updateUI(data) {
    const categoryListDiv = document.querySelector('.categories');
    const taskListDiv = document.querySelector('.tasks');
    categoryListDiv.innerHTML = '';
    taskListDiv.innerHTML = '';
    data.categories.forEach(category => {
        const categoryElement = document.createElement('div');
        categoryElement.innerHTML = `
        <div class="card" style="z-index:-9999;">
            <div class="card-head">
                <p><strong>${category.name.slice(0, 18)}${category.name.length > 18 ? '...' : ''}</strong></p>
                <span class="material-symbols-outlined" id="category-menu">
                    more_vert
                </span>
            </div>
            <p class="Description">${category.description.slice(0, 75)}${category.description.length > 75 ? '...' : ''}</p>
            <p class="stats"><strong>Completed : </strong> ${category.completed_tasks}/${category.total_tasks}</p>
            <a href="/tasks/category-detail/${category.id}">View</a>
            <p class="card-footer">Created : ${category.created_at}</p>
        </div>
        `;
        categoryListDiv.appendChild(categoryElement);
    });
    data.tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.innerHTML = `
        <div class="task ${task.status}" style="z-index:-9999;">
            <a href="/tasks/task-detail/${task.id}">
                <div class="heading">
                    <p class="first">${ task.title }</p>
                    <p class="second ${task.priority}-priority %}">${ task.priority }</p>
                </div>
                <p class="third"><strong>Category : </strong> ${ task.category }</p>
                <p class="fourth"><strong>Start : </strong>${task.date_creation}</p>
                <p class="fifth"><strong>Due : </strong>${task.due_date}</p>
            </a>
        </div>
        `;
        taskListDiv.appendChild(taskElement);
    });
}