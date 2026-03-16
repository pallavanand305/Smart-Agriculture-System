"""
AADS Module — Max-Heap Priority Queue
Schedules farm tasks by urgency score.
Priority Score = 0.5*(1/moisture) + 0.3*(1/days_until_due) + 0.2*pest_risk
"""

class Task:
    def __init__(self, task_id, task_type, zone, moisture, days_until_due, pest_risk=0.0):
        self.task_id       = task_id
        self.task_type     = task_type
        self.zone          = zone
        self.moisture      = moisture
        self.days_until_due = max(days_until_due, 0.01)
        self.pest_risk     = pest_risk
        self.score         = self._compute_score()

    def _compute_score(self):
        return (0.5 * (1 / max(self.moisture, 1)) +
                0.3 * (1 / self.days_until_due) +
                0.2 * self.pest_risk)

    def __repr__(self):
        return f"Task({self.task_type}, zone={self.zone}, score={self.score:.4f})"


class MaxHeap:
    """Max-Heap backed by a Python list. O(log n) insert and extract."""

    def __init__(self):
        self._heap = []

    def insert(self, task: Task):
        self._heap.append(task)
        self._bubble_up(len(self._heap) - 1)

    def extract_max(self) -> Task:
        if not self._heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self._heap) - 1)
        max_task = self._heap.pop()
        self._heapify_down(0)
        return max_task

    def peek(self) -> Task:
        if not self._heap:
            raise IndexError("Heap is empty")
        return self._heap[0]

    def size(self) -> int:
        return len(self._heap)

    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[parent].score < self._heap[i].score:
                self._swap(parent, i)
                i = parent
            else:
                break

    def _heapify_down(self, i):
        n = len(self._heap)
        while True:
            left, right, largest = 2*i+1, 2*i+2, i
            if left  < n and self._heap[left].score  > self._heap[largest].score:
                largest = left
            if right < n and self._heap[right].score > self._heap[largest].score:
                largest = right
            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def all_tasks(self):
        return sorted(self._heap, key=lambda t: -t.score)


# ── Quick demo ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    heap = MaxHeap()
    heap.insert(Task(1, "Irrigation",   "ZoneA", moisture=18, days_until_due=1))
    heap.insert(Task(2, "Fertilize",    "ZoneB", moisture=45, days_until_due=3))
    heap.insert(Task(3, "Pest Control", "ZoneC", moisture=60, days_until_due=2, pest_risk=0.9))
    heap.insert(Task(4, "Irrigation",   "ZoneD", moisture=22, days_until_due=1))

    print("Tasks by priority:")
    while heap.size():
        print(" ", heap.extract_max())
