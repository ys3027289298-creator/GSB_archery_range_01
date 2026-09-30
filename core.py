import json


def new_game():
    return {"items": {}, "load": 0, "capacity": 2, "stock": 100, "metric": 100, "day": 1, "id": 0, "fault": False, "resource": 10, "rate": 2, "clock": 0, "paused": False, "settled": False}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def add(state, item_id, amount):
    if state["settled"]:
        return False
    if item_id in state["items"]:
        return False
    state["items"][item_id] = amount
    state["stock"] -= amount
    return True


def receive(state, item_id):
    if state["settled"]:
        return False
    if state["load"] >= state["capacity"]:
        return False
    state["load"] += 1
    return True


def fee(state, item_id, end_day):
    return (end_day - state["day"]) * state["rate"]


def cancel(state, item_id):
    if state["settled"]:
        return False
    if item_id not in state["items"]:
        return False
    state["stock"] += state["items"].pop(item_id)
    return True


def produce(state, amount):
    if state["settled"]:
        return False
    if state["fault"]:
        return False
    state["stock"] += amount
    return True


def event(state):
    if state["settled"]:
        return state["metric"]
    state["metric"] -= 10
    return state["metric"]


def guard(state, item_id):
    return state["resource"] > 0


def tick(state):
    if state["paused"] or state["settled"]:
        return state["clock"]
    state["clock"] += 1
    return state["clock"]


def settle(state):
    state["settled"] = True
    return True


def main():
    state = new_game()
    print("命令: add/receive/fee/cancel/produce/event/guard/tick/settle/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        try:
            nums = [int(a) for a in args]
            if cmd == "add" and len(nums) == 2:
                ok = add(state, nums[0], nums[1])
            elif cmd == "receive" and len(nums) == 1:
                ok = receive(state, nums[0])
            elif cmd == "fee" and len(nums) == 2:
                ok = fee(state, nums[0], nums[1])
            elif cmd == "cancel" and len(nums) == 1:
                ok = cancel(state, nums[0])
            elif cmd == "produce" and len(nums) == 1:
                ok = produce(state, nums[0])
            elif cmd == "event" and not nums:
                ok = event(state)
            elif cmd == "guard" and len(nums) == 1:
                ok = guard(state, nums[0])
            elif cmd == "tick" and not nums:
                ok = tick(state)
            elif cmd == "settle" and not nums:
                ok = settle(state)
            else:
                ok = False
        except ValueError:
            ok = False
        print("ok" if ok else "fail")


if __name__ == "__main__":
    main()
