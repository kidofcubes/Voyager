
# training loop pseudocode:
```python

iterations = 0
while iterations < max_iterations:
    if completed_tasks.length < warm_up:
        task, context = curriculum.LLM_get_next_task(bot.state().filter(key.warm_up <= completed_tasks.length and 80% chance))
    else:
        questions = curriculum.LLM_get_questions(bot.state())
        answers = curriculum.LLM_get_answers(questions)
        task, context = curriculum.LLM_get_next_task(questions, answers, bot.state().filter(key.warm_up <= completed_tasks.length and 80% chance))
    
    repeat max_task_retry:
        task_code = action_agent.LLM_generate_task_code(task, context, critique, bot.state(), skill_manager.get_relavant_programs(task_context))
        iterations++
        if task_code is valid:
            bot.run(task_code, skill_manager.all_programs)
            critique = critic.LLM_check(bot.state(), task)
            
            if critique == success
                break;
            
    if critique == success:
        skill_manager.add_new_skill(task, task_code, skill_manager.LLM_generate_description(task, task_code))
    else:
        skill_manager.add_failed_skill(task)
    
        
```

# task inference pseudocode:
```python
task = "Get a diamond pickaxe"
sub_tasks = decompose_task(task, bot.status()) #inclues task

while progress < sub_tasks.length:
    next_task = sub_tasks[progress]
    context = "Question: "+"How to "+next_task+"\n Answer: "+curriculum.LLM_get_answers("How to "+next_task)
    repeat max_task_retry:
        task_code = action_agent.LLM_generate_task_code(task, context, critique, bot.state(), skill_manager.get_relavant_programs(task_context))
        iterations++
        if task_code is valid:
            bot.run(task_code, skill_manager.all_programs)
            critique = critic.LLM_check(bot.state(), task)
            
            if critique == success
                break;
    if critique == success:
        progress++
    

```

# training loop sequence diagram:
![graph link for viewing outside of obsidian](https://img.plantuml.biz/plantuml/png/ZLNRJXin47tVhvZ78aebAlK5LIqKL4GLsY9wUKYhbV7E9bOSU_6CI_BtZBsvRBOR85AoNdjyvioPO-UKM0MESriepJx0jN5OMxN4K9vRWuv1KMUok52ixXGXtCwCjUN8t0KLbiLt0J7QD4es_F9BDP7GxjneT5qKa-1Z0pSHYOrte5m5PuuUC12Clpcx15Kp1ZX-1qQUAWNHtmBaiuA4emy9wGH-JvKG2mZavmW1BVvBMUvNqFGH3k7ECqXnZ38UryfOh4fMD5j1EYyh5ci-WLSwXc1qj75UtgkI69lZKYBB3TuRNl313fFtHosJyIQcXRNUD_1PX4Ibfnj2UMcea9j-mDEqtfOg2pR4R8XTAszUHbSLwTjdS8aC3XSCIPidPKiJsshJMqj6AXzctNBhS_hQIHPGaNV6JOeY2_VJiR50KMl4Ybw3w3WrJ31NYtPBG0xY4sQSDqnzR-nuiYrjuurSmnCbzEJhGNsvXNDV8VYwXpXepqjqoR_OSjPfuwwm_V9bh8DX8zpWZplSa-iPzjqco66Me3B9P2LbweJ4hsO3KYC8MDO-p1NlDxTKdSZtQznU1vkGJCPAFTLIAAZWi8B-OGjcCXLkszqGNQCY8UMh84H7m5CSp2gCkba_hRNy3_tAQHihJ4YYAu4riupOg419Q0p11t4MiXQLKbfiEHmCTl9yYde6fcuzILH7EzpAbpOcjrdlb_oATbEjRP63ym5kRz4TIYymOHrTRZw8DeBPvF4X_4XhNS6xN2cTWVrKBpf8ugJSkvrSpnpFiwgIc-TXhM2NolfrY7KMeJYLN_dNUWG0)
```plantuml
@startuml
actor Mineflayer_Client as Mineflayer
Database Skill_Library
Participant Voyager
Participant LLM

group Question and Answers [Only after 15 iterations]
    Voyager -> LLM: What are some relevant questions? + bot state + [failed_tasks]
    note left: (curriculum_qa_step1_ask_questions.txt)
    Voyager <- LLM: [questions]
    loop For each question
        Voyager -> LLM: Question
        note left: (curriculum_qa_step2_answer_questions.txt)
        Voyager <- LLM: Answer
    end
end
Voyager -> LLM: Get next task + bot state + [failed_tasks] + [questions] + [answers]
note left: (curriculum.txt)
Voyager <- LLM: Next task + reasoning

loop Until succeeds, or hits max task retry attempts
    Voyager -> Skill_Library: Get relevant tasks + [questions] + [answers]
    Voyager <- Skill_Library: JS Code of relevant tasks
    Voyager -> LLM: Generate task code + bot state + task + reasoning + critique \n+ Code of relevant tasks + [questions] + [answers]
    note left: (action_template.txt + action_response_format.txt)
    Voyager <- LLM: JS code
    Voyager -> Mineflayer: JS code + [already learned tasks]
    note right: Mineflayer unpauses and runs the JS code
    Voyager <- Mineflayer: Bot state
    note right: Includes things like JS parsing errors, etc (and repauses)
    Voyager -> LLM: Check if successful + bot state + task + [questions] + [answers]
    note left: (critic.txt)
    Voyager <- LLM: Is successful + critique
    
end
group if successful
    Voyager -> LLM: Generate task function description + Task JS code
    note left: (skill.txt)
    Voyager <- LLM: Description for the task function
    Voyager -> Skill_Library: Add new task + Task JS code + Task function description
end

@enduml
```

![graph link for viewing outside of obsidian](https://img.plantuml.biz/plantuml/png/bLNVJnD147w_ls8V8GOJVIH6YVf489hK-4B8PQaBNhZ-u6uRvQs8XMkn5BM0j9XIRGaIeFKN7XNadxdTk_uNpjsMScsle4rwsSpEVVFDp3Tp8ph56ar4L0c7QKn3uqgKJAjudcZo0rKXKOgmxZDA3p75KrWdA3IhgAeyfanfM9kN7WE84bRY65vu6fl7C-3gjusDZKlIZ1PBn55pyyW-pAC9jhrd7nomx8BLoBDArZclMx-hR6sLfxFMQO6T9YSb1ByM6Xgwwu8C8xwTPk_thKRHBfeizHtGcfy-t4CtqFr7J_XYYYtzXFC4gtnrVbJjmckxUCHtbfcnwPJt160qHWbIoJGTHWFXXAOfuOIQYCXpMDOfYT-IiJuhpoM8JfLOLBz9NzB13XvtXWGF256mp7qHNo2B_DYVVNkr1dPUoxKTlFkWTBgkhoPtMyPH_GMq9e1V44UeCoyRtZM9FfFSVq1yoronp2HG5RNgBcKhG_Sey2QlA70mVy6oXzr5E740BBPQOiMT2w68Gjg7QMwiiKp9QYnnOyD9ffXHRovddTewFoZpzNfpQuqPnzrQwP0dg6RbNEYbpTWzxAsmHYuun-wUT-7r0mkKh9qlGGejpukO_XhtgmHOUFg46HNlwh_f-vi1qmrwaIc9n5LCYTiHS6zPDQB7GKn4devf4KpxYtuqX8BplDmGFYTF9uUxphdBbcUIpkAPZvYcp3m7PfTl8fRRuCS6Dqrkv7ZX5LlOPk_UEB_UZeO2WW8bVz1sENi2M2SbPkxQ7vEZeMP-owdLND253AjySOxgx6mT3O0728flr4NGmU2zypd9IrNOFlnRsNrwckpNnt_fI5XJO3tshtLlAA45pzcRvTQOP7POgYgShfSVI6lv3AQ6vtAmSG6qiwL-Wheh-Vxy0W6l6KFW2cLsrU3HRQlPpwDZ3FpGRihI23pXQ_KN)
```plantuml
@startuml
actor Mineflayer_Client as Mineflayer
Database Skill_Library
Participant Voyager
Participant LLM

group 问答 [在第十五复述以后才会开]
    Voyager -> LLM: 有哪些相关问题? + BOT情况 + [失败的目标列表]
    note left: (curriculum_qa_step1_ask_questions.txt)
    Voyager <- LLM: [多个问题]
    group 循环问每个问题
        Voyager -> LLM: 问题
        note left: (curriculum_qa_step2_answer_questions.txt)
        Voyager <- LLM: 答案
    end
end
Voyager -> LLM: 问下一个目标 + BOT情况 + [问题] + [答案] + [失败的目标列表]
note left: (curriculum.txt)
Voyager <- LLM: 目标 + 目标的原因

group 循环等成功了或者到重试次数限制
    Voyager -> Skill_Library: 拿相关的目标的程序 + [问题] + [答案]
    Voyager <- Skill_Library: 相关的目标的程序
    Voyager -> LLM: 生成目标程序 + BOT情况 + 目标 + 目标的原因 + 批判 + 相关的目标的程序 + [问题] + [答案]
    note left: (action_template.txt + action_response_format.txt)
    Voyager <- LLM: JS 程序
    Voyager -> Mineflayer: JS 程序 + [学过的技能]
    note right: Mineflayer 取消游戏暂停和跑JS程序
    Voyager <- Mineflayer: BOT情况
    note right: 也带着JS错误和聊天记录 (也重新暂停)
    Voyager -> LLM: 检查有没有成功 + BOT情况 + 目标 + [问题] + [答案]
    note left: (critic.txt)
    Voyager <- LLM: 有没有成功 + 批判
    
end
group 加入成功
    Voyager -> LLM: 生成目标的函数描述 + JS 程序
    note left: (skill.txt)
    Voyager <- LLM: 目标的函数描述
    Voyager -> Skill_Library: 加新的成功的目标 + JS 程序 + 目标的函数描述
end

@enduml

```