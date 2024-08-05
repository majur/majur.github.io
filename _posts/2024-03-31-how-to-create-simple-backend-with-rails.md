---
title: How to create simple backend with rails
author: juraj
date: 2024-03-31 10:33:00 +0800
categories: [Dev]
tags: [Backend, Ruby, Rails]
math: true
mermaid: true
pin: false
image:
  path: /assets/img/rails-logo.webp
  lqip:
  alt: Ruby on Rails logo
---

A bigger project from my portfolio is a CMS written in Ruby on Rails, which I've called Blog on Rails for now. But I need a few smaller (and sooner finished) projects. The first one is a simple backend for a todo list application. I'm writing it also in Ruby on Rails, but I'm only writing the backend API part.

## Creating a rails application and generating basic files

Ruby on Rails is greate fullstack framework, but for now I building only API. First step is to create Rails app. I use this command:

```bash
rails new todo_rails_backend --api -d sqlite3
```

I'm using `--api` for generating only backend parts. Since I want to use SQLite for the database, I use the command `-d sqlite3`.

Moving to app directory:

```bash
cd todo_rails_backend
```

Next I have to generate Task model:

```bash
rails generate model Task title:string description:text due_date:date completed:boolean
```

This will generate model, test for model and migration. Now I need to generate controller for Task:

```bash
rails generate controller Tasks
```

## Implementation of Tasks controller

### Create Action

Now let's implement a task controller. At the beginning we have an empty database and we need to create records. So let's start with the create action.

```ruby
class TasksController < ApplicationController
  def create
    @task = Task.new(task_params)

    if @task.save
      render json: @task, status: :created, location: @task
    else
      render json: @task.errors, status: :unprocessable_entity
    end
  end

  private
    def task_params
      params.require(:task).permit(:title, :description, :due_date, :completed)
    end
end
```
{: file='app/controllers/tasks_controller.rb'}

We create a new instance of the Task model using the parameters received from the request. Parameters are defined in private method `task_params`. This is done by calling Task.new(task_params).

We attempt to save the newly created task to the database using `@task.save`. 

If the task is successfully saved, backend render the JSON representation of the created task along with the HTTP status `201 Created` using `render json: @task, status: :created`. It also include the `Location` header pointing to the newly created task's URL.

If there are validation errors preventing the task from being saved, we render the JSON representation of the validation errors along with the HTTP status `422 Unprocessable Entity` using `render json: @task.errors, status: :unprocessable_entity`.

**Last few steps before creation of the first task.** We need to add resource to `routes.rb` file:

```ruby
Rails.application.routes.draw do
  resources :tasks
end
```
{: file='routes.rb'}

Run database migration:

```bash
rails db:migrate
```

And start the server:

```bash
rails s
```

Now we can test it in Postman by calling `POST` request on `/tasks` endpoint like this:

```json
POST /tasks
Content-Type: application/json

{
  "task": {
    "title": "Complete project report",
    "description": "Write and submit the project report by Friday",
    "due_date": "2024-04-05",
    "completed": false
  }
}
```

This should return JSON like this with status `201 Created`:
```json
{
   "title": "Complete project report",
    "description": "Write and submit the project report by Friday",
    "due_date": "2024-04-05",
    "completed": false,
    "created_at": "2024-03-30T17:33:41.831Z",
    "updated_at": "2024-03-30T17:33:41.831Z"
}
```

When we open rails console by `rails c` we can see last created post by running this `Task.last`. It should return this:

```bash
#<Task:0x000076a8c7f23160
 id: 1,
 title: "Complete project report",
 description: "Write and submit the project report by Friday",
 due_date: Fri, 5 Apr 2024,
 completed: false,
 created_at: Sat, 30 Mar 2024 17:33:41.831520000 UTC +00:00,
 updated_at: Sat, 30 Mar 2024 17:33:41.831520000 UTC +00:00>
```

### Index and Show Actions

The `index` action retrieves a collection of tasks from the database and returns them as JSON. Additionally, it allows filtering tasks based on their completion status.

```ruby
# GET /tasks
def index
  if params[:completed].present?
    @tasks = Task.where(completed: params[:completed])
  else
    @tasks = Task.all
  end
  render json: @tasks
end
```
{: file='app/controllers/tasks_controller.rb'}

If a `completed` parameter is present in the request, the action filters tasks based on their completion status using `Task.where(completed: params[:completed])`. If the parameter is not present, it retrieves all tasks from the database using `Task.all`.

To get all tasks:

```bash
GET /tasks
```

To get only completed tasks:

```bash
GET /tasks?completed=true
```

To get only incomplete tasks:

```bash
GET /tasks?completed=false
```

The `show` action retrieves a single task from the database by its ID and returns it as JSON.

```ruby
# GET /tasks/1
def show
  render json: @task
end
```
{: file='app/controllers/tasks_controller.rb'}

The action finds the task with the specified ID using `Task.find(params[:id])`. This ID is typically provided in the request URL.

To retrieve a specific task by its ID, you would send a `GET` request to the corresponding endpoint. For example:

```bash
GET /tasks/1
```

### Update Action

The `update` action is responsible for modifying an existing task based on the provided parameters. It finds the task by its ID, updates its attributes, and attempts to save the changes to the database.

```ruby
# PATCH/PUT /tasks/1
def update
  if @task.update(task_params)
    render json: @task
  else
    render json: @task.errors, status: :unprocessable_entity
  end
end
```
{: file='app/controllers/tasks_controller.rb'}

The action finds the task with the specified ID using `Task.find(params[:id])`. This ID is typically provided in the request URL. It attempts to update the task attributes with the parameters provided in the request body using `@task.update(task_params)`. If the task is successfully updated, the updated task object (`@task`) is rendered as JSON using `render json: @task`. If there are validation errors preventing the task from being updated, the validation errors are rendered as JSON along with the HTTP status `422 Unprocessable Entity`.

To update a specific task, you would send a `PATCH` or `PUT` request to the corresponding endpoint (`/tasks/:id`) with the updated task parameters in the request body.

```json
PATCH /tasks/1
Content-Type: application/json

{
  "task": {
    "title": "Updated task title",
    "description": "Updated task description",
    "due_date": "2024-04-10",
    "completed": true
  }
}
```

The `update` action allows users to modify task details, providing flexibility in managing tasks within the application. Next, we'll explore the `destroy` action for removing tasks from the system.

### Destroy Action

The `destroy` action handles the deletion of a specific task from the database. It finds the task by its ID, removes it from the database, and returns a successful response indicating the deletion.

```ruby
# DELETE /tasks/1
def destroy
  @task.destroy
end
```
{: file='app/controllers/tasks_controller.rb'}

The action finds the task with the specified ID using `Task.find(params[:id])`. It removes the task from the database using `@task.destroy`. This operation deletes the task record from the database. Since there's no need to return any specific data after successful deletion, the action does not render a JSON response. The default response with status `200 OK` is sent back to the client.

To delete a specific task, you would send a `DELETE` request to the corresponding endpoint (`/tasks/:id`), specifying the ID of the task to be deleted.

```json
DELETE /tasks/1
```

The `destroy` action provides a way to remove tasks from the system, completing the CRUD operations for tasks in the Rails application. These actions collectively enable users to manage tasks effectively within the application.

## Conclusion

In this blog post, we've explored the implementation of a Rails backend controller for managing tasks. We've covered each CRUD (Create, Read, Update, Delete) action in detail, discussing their purpose, implementation, and example usage.

By breaking down the controller into smaller parts and explaining each action separately, we aimed to provide a clear understanding of how to handle task management within a Rails application. From retrieving tasks to creating, updating, and deleting them, these actions form the foundation of a robust task management system.

Repository with this API backend is [here](https://github.com/majur/todo_rails_backend). You can find my CV [here](/cv/), and if you want to arrange a call with me please send me an email to juraj@matase.sk