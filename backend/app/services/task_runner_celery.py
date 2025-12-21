from app.core.celery_app import celery_app
# ... existing imports ...

# ... existing code ...

@celery_app.task
def run_task_celery(task_id: int):
    # This function will be executed by Celery worker
    # Need to create a new event loop or run synchronous code
    # For simplicity, we might just call the async runner via asyncio.run()
    import asyncio
    
    # Re-instantiate objects (fetch from DB in real scenario)
    task = TestTask(id=task_id) 
    cases = [] 
    
    runner = TaskRunner(task, cases)
    asyncio.run(runner.run())
