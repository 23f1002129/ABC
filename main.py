import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS as required by the assignment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/execute")
async def execute_task(q: str):
    # 1. Ticket Status
    ticket_match = re.search(r"ticket (\d+)", q, re.IGNORECASE)
    if ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": int(ticket_match.group(1))})
        }

    # 2. Meeting Scheduling (Extracts: Date, Time, Room)
    # Pattern: on YYYY-MM-DD at HH:MM in Room X
    meeting_match = re.search(r"on ([\d-]+) at ([\d:]+) in (.+)", q, re.IGNORECASE)
    if "schedule" in q.lower() and meeting_match:
        room = meeting_match.group(3).strip(".")
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": room
            })
        }

    # 3. Performance Bonus (Must come before generic expense check)
    bonus_match = re.search(r"employee (\d+) for (\d+)", q, re.IGNORECASE)
    if "bonus" in q.lower() and bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # 4. Expense Balance
    expense_match = re.search(r"employee (\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and expense_match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(expense_match.group(1))})
        }

    # 5. Office Issue Reporting
    issue_match = re.search(r"issue (\d+) for the (.+) department", q, re.IGNORECASE)
    if issue_match:
        dept = issue_match.group(2).strip(".")
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept
            })
        }

    return {"error": "Query did not match any pre-defined functions"}
