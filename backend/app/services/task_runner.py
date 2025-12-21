import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test_case import TestCase, TestType
from app.models.task import TestTask, TaskStatus
from app.models.report import TestReport

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, task_id: int, test_cases: List[TestCase]):
        self.task_id = task_id
        self.test_cases = test_cases
        self.results = []

    async def run(self, db: AsyncSession):
        logger.info(f"Starting task {self.task_id}")
        
        # Fetch task to ensure it's attached to current session if needed, 
        # or just update by ID.
        task = await db.get(TestTask, self.task_id)
        if not task:
            logger.error(f"Task {self.task_id} not found")
            return

        task.status = TaskStatus.RUNNING
        task.start_time = datetime.utcnow()
        await db.commit()
        
        passed_count = 0
        failed_count = 0
        skipped_count = 0

        for case in self.test_cases:
            try:
                result = await self.execute_case(case)
                self.results.append(result)
                if result["status"] == "passed":
                    passed_count += 1
                elif result["status"] == "failed":
                    failed_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                logger.error(f"Error running case {case.id}: {e}")
                self.results.append({
                    "case_id": case.id,
                    "status": "failed",
                    "error": str(e)
                })
                failed_count += 1

        logger.info(f"Task {self.task_id} completed")
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.utcnow()
        
        # Create Report
        report = TestReport(
            task_id=self.task_id,
            total_cases=len(self.test_cases),
            passed_cases=passed_count,
            failed_cases=failed_count,
            skipped_cases=skipped_count,
            details=self.results
        )
        db.add(report)
        await db.commit()
        
        return self.results

    async def execute_case(self, case: TestCase) -> Dict[str, Any]:
        if case.type == TestType.API:
            return await self.run_api_test(case)
        elif case.type == TestType.UI:
            return await self.run_ui_test(case)
        elif case.type == TestType.PERFORMANCE:
            return await self.run_performance_test(case)
        else:
            raise ValueError(f"Unknown test type: {case.type}")

    async def run_api_test(self, case: TestCase) -> Dict[str, Any]:
        import httpx
        data = case.data
        method = data.get("method", "GET")
        url = data.get("url")
        headers = data.get("headers", {})
        body = data.get("body")
        
        async with httpx.AsyncClient() as client:
            start_time = asyncio.get_event_loop().time()
            try:
                response = await client.request(method, url, headers=headers, json=body)
                duration = asyncio.get_event_loop().time() - start_time
                
                # Simple assertion logic (expand as needed)
                passed = True
                if response.status_code >= 400:
                    passed = False
                
                return {
                    "case_id": case.id,
                    "type": "api",
                    "status": "passed" if passed else "failed",
                    "status_code": response.status_code,
                    "duration": duration,
                    "response": response.text[:1000] # Truncate for storage
                }
            except Exception as e:
                return {
                    "case_id": case.id,
                    "type": "api",
                    "status": "failed",
                    "error": str(e)
                }

    async def run_ui_test(self, case: TestCase) -> Dict[str, Any]:
        # For UI tests, we might generate a temporary python script and run it with pytest or direct playwright
        # Here is a simplified direct execution example using playwright asyncio API
        from playwright.async_api import async_playwright
        
        data = case.data
        script = data.get("script") # Assume we have the script content or path
        
        # If script is raw code, we might need to exec it or write to file.
        # For security and complexity, usually we write to a file and run pytest.
        # But for this example, let's assume we launch a browser and visit a URL if simple, 
        # or just return a placeholder if it's complex script execution.
        
        # Simplified: Visit URL and take screenshot
        url = data.get("url")
        if not url:
             return {"case_id": case.id, "status": "skipped", "reason": "No URL provided for UI test"}

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            try:
                await page.goto(url)
                title = await page.title()
                # await page.screenshot(path=f"screenshot_{case.id}.png")
                await browser.close()
                return {
                    "case_id": case.id,
                    "type": "ui",
                    "status": "passed",
                    "title": title
                }
            except Exception as e:
                await browser.close()
                return {
                    "case_id": case.id,
                    "type": "ui",
                    "status": "failed",
                    "error": str(e)
                }

    async def run_performance_test(self, case: TestCase) -> Dict[str, Any]:
        # Performance tests usually run for a duration. 
        # We would trigger a locust process here.
        import subprocess
        
        # This is a placeholder for triggering locust
        # In real world, we might generate a locustfile.py based on config
        return {
            "case_id": case.id,
            "type": "performance",
            "status": "triggered",
            "info": "Locust test triggered (mock)"
        }
