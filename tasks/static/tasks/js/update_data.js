//Here i'll get data and update ui accordingly
//...
/*function updateUI(data) {
    const categoryListDiv = document.querySelector('.categories');
    const taskListDiv = document.querySelector('.tasks');
    categoryListDiv.innerHTML = '';
    taskListDiv.innerHTML = '';
    data.categories.forEach(category => {
        const categoryElement = document.createElement('div');
        categoryElement.innerHTML = `
        <div class="card" style="z-index:-9999;">
            <div class="card-head">
                <p><strong>${category.name}</strong></p>
                <span class="material-symbols-outlined" id="category-menu">
                    more_vert
                </span>
            </div>
            <p class="Description">${category.description}</p>
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

// Initial call to fetch updates
fetchUpdates();

// Poll for updates every 5 seconds
//setInterval(fetchUpdates, 5000);*/