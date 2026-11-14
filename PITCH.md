# PITCH.md

Read this out loud while you rehearse. Every number below comes from the code on `main` (seed 42, GPU cloud mode), checked Sun Nov 8 against the running app. Re-check them after any planner or cost-model change.

**Name:** DC Router

**One-liner:** *An AI maintenance agent for GPU data centers. Nemotron decides when each job runs, weighing downtime priced in GPU-market dollars against failure risk; our code does the math and won't let it overheat the hall.*

**Problem statement (NMC² format, say it word for word in beat 1):**
> **When** maintenance takes racks offline in a GPU data center, **the operations lead struggles to** decide what goes down and when, **because** they can't see what each lost GPU-hour is worth today, or what the work does to cooling. **Our solution helps them** schedule every job at its cheapest safe hour, **improving** two numbers: overheat hours, and dollars lost each week.

Measured on the demo week: overheat hours **5 → 0**; dollars lost **$31,867 → $18,223** (overheats priced as outages at an assumed rate). Over 100 simulated weeks: ASAP overheats in 59, ours in 0; median saving about $3,000 a week per hall.

**The rule we repeat:** *Nemotron makes the calls. Code does the math.*

---

## Table demo: 3 min demo + 2 min Q&A, all three of us

### Roles
| Who | Job |
|---|---|
| **Loki** | Driver and narrator. Hands on the keyboard and mouse the whole time, says every line below. |
| **Nandhan** | Q&A: optimizer, thermal sim, 3D hall, UI. Steps in if the UI misbehaves. |
| **Fawaz** | Q&A: price data and the negotiation. Timekeeper (signals at 1:45 and 2:45). Holds the backup video and the phone hotspot. |

Q&A hand-off line: *"Nandhan built the optimizer, he'll take that"* / *"Fawaz built the negotiation."* Answer in 1-2 sentences, then stop.

### Set the screen before judges arrive
1. Backend running, page loaded at `http://localhost:8000`, one warm-up Nemotron request already sent.
2. Press **R** (replay), then **→** eight times so the clock reads **Mon 08:00** (arrows also pause). Click the **ASAP** button.
3. Close any key-moment card. Browser zoom so the whole right panel down to **Trigger alarm** is visible.

Keyboard: **Space** play/pause · **← →** one hour (pauses) · **Shift+→** six hours · **R** replay. Switch plans by **clicking** the "Our plan" / "ASAP" buttons (Tab only works when nothing has focus).

Measured on the real app: the UPS-B request and the alarm run each take about 15–30 s live (alarm: "Done in 28 s"); the handoff and the negotiation follow on their own within about 20 s more.

### The script (a story in six beats)

Spoken at a normal pace this is about 2:45, which leaves room for clicks and the Nemotron wait. **Bold** is what to stress. *Italics in brackets* is what your hands do.

**Beat 1: The stakes and the problem statement (0:00–0:25)**
*[Screen already at Mon 08:00, ASAP selected. Point at the hall.]*
> "Picture running operations at a GPU data center. Every rack you take down is GPUs not earning: an H100 rents for **about four dollars an hour**, and this simulated hall has **1,280 of them**. **When** maintenance takes racks offline, **the operations lead struggles to** decide what goes down and when, **because** they can't see what each lost GPU-hour is worth today, or what the work does to cooling. **Our solution helps them** schedule every job at its **cheapest safe hour**, **improving two numbers: overheat hours, and dollars lost each week.** Today, the default is just: do it ASAP."

**Beat 2: The barrier, live (0:25–0:45)**
*[Press → three times to Mon 11:00. Point at the red zones, then the overheat count. Not at the dollar cards.]*
> "Watch what ASAP does. Two cooling units that back each other up, CRAC-2 and CDU-3, both go down **Monday at nine**. Our hour-by-hour thermal simulation shows zones two and three going past **32 degrees: five hours of overheating**. That's the missed warning NMC² talks about: routine maintenance turning into an outage."

**Beat 3: Our plan moves both numbers (0:45–1:10)**
*[Click **Our plan**: the hall goes calm. Drag the week bar all the way right. Point at "GPU-hours offline", then "Overheats".]*
> "Our plan does the **same six jobs, the same 4,320 GPU-hours offline**. We only change *when*. The optimizer prices every hour using **real H100 rental prices from 46 providers**, adds the risk that grows while a job waits, and runs the thermal sim on **every slot it considers**. Overheat hours: **five down to zero.** Dollars lost: counting those overheats as outages at our assumed rate, that's **$18,223 against $31,867** this week."
*[Close the card.]*

**Beat 4: A new job, and Nemotron plans it (1:10–1:50)**
*[Click the **UPS-B battery swap** chip. Point at each trace line as it lands; stop on **Chose a slot**.]*
> "Then a vendor calls: UPS-B battery swap, three hours, only Wednesday or Friday. **Nemotron takes over as the planner.** It finds UPS-B's racks, turns 'Wednesday or Friday' into hours, asks our pricing tool for its options (cheapest safe, earliest, wait a day) and **picks one, with its reason**. Then it **checks its own plan against the simulation** before committing. That's Nemotron beyond a chatbot: **Nemotron makes the calls, our code does the math**, and any number a tool didn't return gets thrown out."

**Beat 5: An alarm, and nobody types (1:50–2:40)**
*[Click **Trigger alarm**. Point at the red alarm card, then the trace. When the panel says **Done**, click **Pause** (or × on the end card). Point at the islands and the drone, scroll the right panel to the handoff and the offer, click **Accept**.]*
> "Wednesday, 2 PM: CRAC-3 is vibrating at **three times normal**. Nobody types anything. Nemotron reads the alarm, sees that **waiting a day costs $210 more**, schedules the repair now, and **writes the handoff for the next shift**: which racks, which temperatures to watch. No more unclear handoffs. Those racks are sold to customers, so our procurement agent asks **Nebius and CoreWeave** for replacement compute: simulated offers, capped at a **break-even our code sets**. CoreWeave stops at $3.62, so it walks. Nebius takes **$3.39, cheaper than leaving the customer short**. A person approves."
*[Click Accept.]*

**Beat 6: Why it matters (2:40–3:00)**
*[Hands off the keyboard. Look at the judges.]*
> "Back to our two numbers. Across **100 simulated weeks**, ASAP overheated the hall in **59**. Ours in **none**, saving a median of about **$3,000 a week per hall: roughly $160,000 a year**, in our simulation. GPU compute is becoming a priced commodity. Data centers need to schedule around that price, and this does it."

**Running long?** Cut, in order: the commodity line (beat 6), "adds the risk that grows while a job waits" (beat 3), the CoreWeave walk-away (beat 5).
**Running short?** Add after beat 2: "More than half of operators say their last major outage cost over $100,000."
**Nemotron slow?** Keep pointing at trace lines as they land and describe each one. Never stand in silence.

### 60-second version (a judge has one minute)
*[Mon 11:00: click ASAP, then Our plan.]* "When maintenance takes GPU racks offline, ops leads struggle to pick the timing because they can't see what each lost GPU-hour is worth, or what the work does to cooling. We schedule every job at its cheapest safe hour, cutting overheat hours and dollars lost. Done ASAP, two cooling jobs overlap and the hall overheats five times; our planner does the same work with zero, priced on real GPU rental data." *[Click Trigger alarm.]* "And when an alarm fires, nobody types: Nemotron prices fixing now against waiting, schedules the repair, writes the shift handoff, and our agent buys replacement compute under a break-even our code sets. Nemotron makes the calls; code does the math."

---

## Tie it to the prompts (say these exact words)

**NMC² "Keep the world running":** *"A missed warning, an unclear handoff, or the wrong information at the wrong time can turn a small issue into a major disruption. Help data center teams stay one step ahead."*

| Their words | Our moment | Line |
|---|---|---|
| "Missed warning" | ASAP overheats Z2/Z3 Monday | "We catch the overheat before it happens. The optimizer never picks a slot that crosses 32 degrees." |
| "Wrong information at the wrong time" | Summary card, $ per slot | "The ops lead doesn't know what a lost GPU-hour is worth today. We put that price on every hour." |
| "Unclear handoff" | Handoff after the alarm | "The next crew gets what, when, which racks, which temperatures to watch, and the risk if it slips." |
| "Stay one step ahead" | Alarm with no human | "Nobody typed that. The agent had the repair scheduled and cover lined up." |

**NVIDIA "Use Nemotron beyond a chatbot":** multi-step workflows (agents that plan and execute), tool integration, real-world applicability.

| Their words | Our moment | Line |
|---|---|---|
| "Agents that plan and execute" | Trace: compare → **choose** → simulate → re-plan | "It weighs priced options and picks one, then checks its own plan against the simulation." |
| "Tool integration" | 9 tools in the trace | "Nine tools. Every number on screen came from a tool, not the model." |
| "Real-world applicability" | Real H100 prices; the alarm | "Real market prices from 46 providers, and it acts on an alarm with no prompt." |

---

## If it breaks
- **Nemotron slow (over 30 s):** keep narrating the trace as steps arrive. "It's calling the hosted Nemotron endpoint live."
- **Nemotron errors or is rate-limited:** the rehearsed chips fall back to the verified plan (the trace says `fallback`). Say: "The endpoint's rate-limited; this is the same request through our fallback. The plan and numbers come from our code either way."
- **Backend down:** the UI falls back to the saved plans. "The result is deterministic, so this is the exact backend output."
- **3D stutters:** point at the right panel. "The scoreboard is the point: our plan against ASAP, in dollars and overheats."
- **Total failure:** Fawaz plays the backup video.

## Don't
Team intros. Clicking around to find things. Opening Details unless a judge asks "where do the savings come from" (then: **Details**, "Where the savings come from"). Saying "trained", "fine-tuned", "live price feed", or that futures are "trading". Calling Nemotron a parser or a chatbot.

---

## Requests (must match `backend/app/demo_requests.py`)

| # | Type exactly | Result | Quote $? |
|---|---|---|---|
| 1 | UPS-B battery swap, 3 hrs, vendor only Wed or Fri | Z4, Wed 02:00–05:00, no violations; week $22,454.73 vs ASAP $36,186.60 | Yes |
| 2 | CRAC-4 filter and belt service, 4 hours, weekdays 8am to 6pm | Z4, Mon 09:00–13:00, no violations | Yes |
| 3 | PDU row C breaker inspection, 2 hours, weekend only | Z3, Sat 06:00–08:00, no violations | **No.** ASAP can't schedule weekend jobs, so the saving compares different work |

**Unscripted, for a judge who wants to type:** "Swap the fan tray on CRAC-1, about 2 hours, any weekday afternoon" (tested live, clean). Live runs take 15–40 s; narrate the trace while it works.

For the 3 rehearsed requests, Nemotron's parse is checked against a verified task and replaced only if it differs (the trace shows `guardrail:pinned_demo_task`). Unscripted requests use Nemotron's parse as-is.

---

## Q&A (2 minutes: expect 3 or 4 questions; owner in brackets)

**1. "What does Nemotron actually decide, and what's code?"** [Loki]
"Nemotron decides; code computes. It picks the tools, picks a slot from priced options with a reason, decides to re-plan when the simulation flags a problem, and handles alarms with no prompt. Code computes every number and refuses unsafe picks, so it can choose but can't overheat the hall or invent a dollar figure."

**2. "Isn't that just argmin? It always picks the cheapest."** [Loki]
"Not always. Its instructions are cheapest safe unless the operator asks for something else, so 'as soon as possible' gets the earliest safe slot instead, with its reason. The math is code on purpose: we want the model's judgment, not its arithmetic." *(Only demo this live after testing an "as soon as possible" request 3 times.)*

**3. "Where do the savings come from?"** [Nandhan]
"Mostly from avoiding overheats, priced at an assumed outage rate. Price timing alone saves about $177 this week, because real H100 prices barely move in a week. That's why we lead with zero overheats versus five."

**4. "Is the week rigged for ASAP to fail?"** [Nandhan]
"We ran 100 random seeded weeks. ASAP overheated in 59; ours in 0, which is by construction since every slot is checked against the sim. All inside our simulation, not a real hall."

**5. "What's real and what's simulated?"** [Fawaz]
"Prices are real: weekly H100 rental history from 46 providers, GetDeploying's open dataset. The hall, backlog, thermal model, alarm, and the provider offers are simulated, and every assumed number is labeled in `config.py`."

**6. "Is the negotiation AI?"** [Fawaz]
"Not yet, and we say so. It's code-bounded rules: an opening ask from the market price, a floor, 5% steps, accept, counter or walk. Next is Nemotron choosing those moves inside the same limits, so no model ever sets a price."

**7. "Why buy compute instead of paying the SLA credit?"** [Fawaz]
"Not covering loses the contract revenue and owes a 10% credit: 1.1 times our $3.25 contract rate, so $3.575 break-even. Nebius at $3.39 saves $62 on this incident and the client keeps their hours."

**8. "Who's the user, and how do you know they have this problem?"** [Loki]
"The operations lead planning a GPU hall's week of maintenance. Honestly, we haven't interviewed one; our evidence is public: 57% of operators say their last major outage cost over $100K, and most GPU cloud capacity is pre-sold, so missed hours carry penalties."

**9. "How's this different from a CMMS or ticketing tool?"** [Loki]
"Those track work orders. We decide when to do the work, priced in compute-market dollars and checked against cooling. Last year's NMC² winners built ticketing and routing; none priced downtime."

**10. "Hardest technical problem?"** [Nandhan]
"Making 'never overheats' true by design: the optimizer runs the hour-by-hour thermal sim on every candidate slot, in about 17 ms per plan. Second: keeping the LLM from ever producing a number. Any explanation with a number the tools didn't return gets replaced."

**11. "Did you fine-tune Nemotron?"** [Loki]
"No. It's hosted Nemotron with tool definitions, and guardrails catch its mistakes. Fine-tuning a smaller Nemotron is next, and our tools already produce the correct labels for training data."

**12. "What breaks at scale?"** [Nandhan]
"First the free Nemotron endpoint's rate limit, since each request makes several model calls. Then the slot search, which grows with tasks times slots times sims; a full fleet needs a solver like OR-Tools, real telemetry, and a live price feed."

**13. "Another week?"** [anyone]
"Real telemetry instead of the simulated hall, a live price feed, Nemotron choosing the negotiation moves, and a fine-tuned smaller Nemotron."

If you don't know: "We haven't tested that. Here's how we'd find out…" Judges trust that.

---

## Before you go on (demo machine)
- [ ] `cd backend && .venv/bin/uvicorn app.main:app` running; http://localhost:8000 loads
- [ ] `NVIDIA_API_KEY` in `backend/.env`; one warm-up request sent
- [ ] Screen set to Mon 08:00, ASAP (see "Set the screen")
- [ ] Notifications off, extra tabs closed, laptop charged, hotspot ready
- [ ] Backup video open in a tab (Fawaz)
- [ ] Rehearse 3 times with a timer; cut any line that pushes past 3:00
