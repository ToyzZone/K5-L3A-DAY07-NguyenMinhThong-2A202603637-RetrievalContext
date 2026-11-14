# Review sheet: rerank-dense / dev

Fill `reviews.json`: `answer_grade` 0/1/2 (answerable; abstain = 0), `abstention_correct` true/false (unanswerable), one true/false per citation in `citation_support` (does that chunk support the claim?), and a short `reason`.

## q01 (answerable)

**Question:** What daily sodium limit does a healthy eating pattern set for adults?

**Expected:** Less than 2,300 milligrams per day.

- gold: fm7-22-2020 p85: "Healthy eating patterns limit sodium to less than 2,300 milligrams per day for adults."

**Searches:** ['healthy eating pattern daily sodium limit adults sodium limit per day 2300 mg guidelines']

**Status:** answered  
**Answer:** Less than 2,300 milligrams per day for adults [fm7-22-2020:p085:para:00]

> **[fm7-22-2020:p085:para:00]** (data/pdf/fm7-22-2020.pdf p85) Nutritional Readiness 8-15. Soldiers need to limit sodium consumption. Healthy eating patterns limit sodium to less than 2,300 milligrams per day for adults. Sodium is an essential nutrient and is needed by the body in relatively small quantities, provided that substantial sweating does not occur. 8-16. Soldiers need to limit alcohol consumption. In the strictest sense, alcohol is not a performance nutrient. If Soldiers consume alcohol, it should be in moderation —up to one drink per day for women and up to two drinks per day for men —and only by adults of legal drinking age. One alcoholic drink -equivalent consists of— • 12 fluid ounces of regular beer (5 percent alcohol). • 5 fluid ounces of wine (12 percent alcohol).

## q02 (answerable)

**Question:** How long is the H2F program in Basic Combat Training?

**Expected:** 10 weeks.

- gold: fm7-22-2020 p32: "The 10-week H2F program for BCT provides foundational readiness and fundamental physical and mental skills."

**Searches:** ['Basic Combat Training H2F program duration how long FM 7-22']

**Status:** answered  
**Answer:** The H2F program for BCT is 10 weeks long [fm7-22-2020:p032:para:00].

> **[fm7-22-2020:p032:para:00]** (data/pdf/fm7-22-2020.pdf p32) BASIC COMBAT TRAINING 2-6. The 10-week H2F program for BCT provides foundational readiness and fundamental physical and mental skills. New Soldiers report to BCT with various levels of potential. The first weeks of training focus on general progression of physical readiness. To minimize the risk of injury, Soldiers must perform exercises correctly, precisely, and with gradually increasing intensity. To imprint the motor skills required for fundamental physical demand tasks, Soldiers repeat the exercises and drills, like the common Soldier tasks, as frequently and with as much attention to detail as possible. The schedules in this doctrine, when executed to standard, provide the proper training intensity and volume to improve training and testing outcomes and control attrition.

## q03 (answerable)

**Question:** Which energy pathway fuels very short, high-power efforts, and for how many seconds?

**Expected:** The phosphagen pathway (stored ATP and phosphocreatine), for about 5-10 seconds.

- gold: fm7-22-2020 p44: "In the phosphagen pathway, adenosine triphosphate stored in the muscle and another molecule called phosphocreatine provide the energy for very short duration (5-10 seconds), high intensity or high power activities."

**Searches:** ['very short high-power efforts energy pathway seconds ATP-PC phosphagen system FM 7-22']

**Status:** answered  
**Answer:** The phosphagen pathway fuels very short, high-intensity or high-power activities, for 5-10 seconds [fm7-22-2020:p044:para:05].

> **[fm7-22-2020:p044:para:05]** (data/pdf/fm7-22-2020.pdf p44) PHOSPHAGEN PATHWAY 4-7. In the phosphagen pathway, adenosine triphosphate stored in the muscle and another molecule called phosphocreatine provide the energy for very short duration (5-10 seconds), high intensity or high power activities. These might include three to five second sprints, the Seated or Standing Power Throw, or maximum repetition lifts. This type of training rapidly depletes energy available in the muscle cells that require long rest periods to re-energize. If Soldiers do not rest enough or are forced to keep going at this level of intensity, the loss of adenosine triphosphate causes degraded performance. Depletion of the phosphagen pathway will force the use of other energy pathways and those pathways will begin to predominate.

## q04 (answerable)

**Question:** Which muscle fibers hold up best against fatigue, and what do they give up in return?

**Expected:** Type I fibers; they contract more slowly and generate less force.

- gold: fm7-22-2020 p47: "Type I fibers are more resistant to fatigue than the others , but Type I fibers have a slower contractile speed and generate less force."

**Searches:** ['muscle fibers fatigue resistant give up force speed document type I type II oxidative glycolytic']

**Status:** answered  
**Answer:** Type I fibers hold up best against fatigue [fm7-22-2020:p047:para:00]. In return, they have a slower contractile speed and generate less force [fm7-22-2020:p047:para:00].

> **[fm7-22-2020:p047:para:00]** (data/pdf/fm7-22-2020.pdf p47) Physiology Figure 4-1. Fiber type training Type I 4-20. Muscle contractions during low -intensity endurance efforts are mainly assigned to Type I or slow oxidative (known as SO) fibers. These fibers are smaller with more mitochondria (parts of the cell that assist with energy production) and capillaries (blood vessels) surrounding them to deliver more oxygen to the fiber. Type I fibers are more resistant to fatigue than the others , but Type I fibers have a slower contractile speed and generate less force.

## q05 (answerable)

**Question:** What dangerous condition can result from drinking too much water?

**Expected:** Hyponatremia: excessive dilution of sodium in the blood.

- gold: fm7-22-2020 p91: "Overhydrating can cause excessive dilution of sodium in the blood, a potentially life-threatening condition called hyponatremia."
- gold: fm7-22-2020 p93: "Too much wa ter can result in hyponatremia."
- gold: fm7-22-2020 p163: "It is possible to drink too much water and become overhydrated or hyponatremic."

**Searches:** ['too much water dangerous condition drinking too much water hyponatremia FM 7-22 physical activity guidelines WHO']

**Status:** answered  
**Answer:** Hyponatremia [fm7-22-2020:p163:para:03]

> **[fm7-22-2020:p163:para:03]** (data/pdf/fm7-22-2020.pdf p163) HYPONATREMIA It is possible to drink too much water and become overhydrated or hyponatremic. Be sure to limit intake to no more than 11⁄2 quarts per hour (48 ounces) during sustained exertion. Clothing 14-13. Leaders ensure that the clothing is comfortable for the climate and bright or reflective enough for outdoor activity conducted in the dark on roadways or sidewalks. Recruits should never wear rubberized or plastic suits, facemasks , or other restrictive breathing devices during exercise or physical assessments. Personal audio devices and earphones are appropriate for indoor activity . Leaders discourage these devices for outdoor activity where they can reduce situational awareness and increase the risk of injury from other pedestrians and traffic.

## q06 (answerable)

**Question:** When building a ruck marching program, above what load relative to body weight should increases be made with caution?

**Expected:** Above 30 percent of body weight.

- gold: fm7-22-2020 p70: "Loads above 30 percent of body weight should be increased with caution."

**Searches:** ['ruck marching program load relative to body weight increases should be made with caution above what load body weight FM 7-22']

**Status:** answered  
**Answer:** Loads above 30 percent of body weight should be increased with caution [fm7-22-2020:p070:para:00].

> **[fm7-22-2020:p070:para:00]** (data/pdf/fm7-22-2020.pdf p70) RUCK MARCHING 7-9. This section illustrates how to develop a program to train for the occupational task of ruck marching. A combat arms unit preparing for dismounted operations during an upcoming deployment uses the following principles and template to develop a training approach. The four-week ruck marching program outlined in table 7-2 and table 7-3 uses the following considerations to develop the first mesocycle in a longer training schedule: • Once per week progressive ruck march: progress one factor each week of either weight of the load, distance of the march, speed of the march, gradient of the terrain or roughness of the terrain. • Loads above 30 percent of body weight should be increased with caution.

## q07 (answerable)

**Question:** How much carbohydrate should a pre-exercise meal contain, and how long before exercise should it be eaten?

**Expected:** 1 to 4 grams of carbohydrate per kilogram of body weight, eaten 1 to 4 hours before exercise.

- gold: fm7-22-2020 p88: "Research suggests a pre-exercise meal containing 1 to 4 grams of carbohydrate per kilogram of body weight, consumed 1 to 4 hours prior to exercise provides improved performance."

**Searches:** ['pre-exercise meal carbohydrate how long before exercise eaten grams per kilogram 1-4 hours']

**Status:** answered  
**Answer:** A pre-exercise meal should contain 1 to 4 grams of carbohydrate per kilogram of body weight and be consumed 1 to 4 hours before exercise [fm7-22-2020:p088:para:01].

> **[fm7-22-2020:p088:para:01]** (data/pdf/fm7-22-2020.pdf p88) 8-33. Research suggests a pre-exercise meal containing 1 to 4 grams of carbohydrate per kilogram of body weight, consumed 1 to 4 hours prior to exercise provides improved performance. Table 8-1 provides examples of pre-exercise meals. If unable to consume a meal prior to early morning exercise, consuming approximately 30 grams of easily digested carbohydrate-rich food or fluid (for example, banana, applesauce, or toast with peanut butter) one hour prior to exercise is beneficial. Table 8-1. Examples of pre-exercise meals Time Between Eating and Performance Suggested Pre-Exercise Meals 1 hour or less before exercise Choice of:

## q08 (answerable)

**Question:** In the endurance heart rate zones table, what percentage of maximum heart rate is zone 2, and what level of effort is it?

**Expected:** 60-70% of HRmax; aerobic endurance at a moderate level of effort.

- gold: fm7-22-2020 p66: "2 60–70 Aerobic endurance Moderate"

**Searches:** ['endurance heart rate zones table zone 2 percentage of maximum heart rate level of effort']

**Status:** answered  
**Answer:** Zone 2 is 60–70% of maximum heart rate, and its level of effort is Moderate [fm7-22-2020:p066:para:01]

> **[fm7-22-2020:p066:para:01]** (data/pdf/fm7-22-2020.pdf p66) Table 6-5. Endurance heart rate zones, fitness components, and levels of effort Zone % HRmax Fitness Component Level of Effort % of Total Endurance Training Distance / Time 5 90–100 Anaerobic explosive speed Maximum 10 200 m / 0:30 4 80–90 Anaerobic endurance Very Hard 30 400 m / 1:15 3 70–80 Aerobic endurance Hard 10 800 m / 3:45 2 60–70 Aerobic endurance Moderate 40 1MR / 7:30 1 50–60 Active recovery Easy 10 2MR / 20:00 HRmax heart rate maximum m meter MR mile run

## q09 (answerable)

**Question:** In the Nutritional Readiness chapter, how much caffeine from tea or coffee can a Soldier have without negatively affecting hydration status?

**Expected:** A small amount, under 200 milligrams; more caffeine may negatively affect fluid balance.

- gold: fm7-22-2020 p89: "A small amount of caffeine in tea or coffee (< 200 milligrams) should not negatively affect hydration status, but if Soldiers drink more caffeine, their fluid balance may be negatively affected."

**Searches:** ['Nutritional Readiness caffeine tea coffee hydration status Soldier amount can have without negatively affecting hydration']

**Status:** answered  
**Answer:** A small amount of caffeine in tea or coffee (< 200 milligrams) should not negatively affect hydration status [fm7-22-2020:p089:para:03].

> **[fm7-22-2020:p089:para:03]** (data/pdf/fm7-22-2020.pdf p89) Fluid Recommendations 8-38. Fluid requirements can vary from 2–16 liters per day depending on workload, level of heat stress, and sweat rate. Sweat loss varies depending on age, training, and acclimation status, exercise intensity and duration, air temperature, humidity, wind velocity, cloud cover, clothing, and individual sweat rates. 8-39. On average, 20–25 percent of fluid intake comes from food and 75 –80 percent from beverages. Plain water, coffee, tea, soups, fruits, and vegetables provide fluids to support hydration. A small amount of caffeine in tea or coffee (< 200 milligrams) should not negatively affect hydration status, but if Soldiers drink more caffeine, their fluid balance may be negatively affected.

## q10 (answerable)

**Question:** When can a recruit increase the weight for a strength exercise, and by how much?

**Expected:** After completing two repetitions over the repetition goal for two consecutive workouts; increase by five to ten percent for the next strength session.

- gold: fm7-22-2020 p164: "For strength training, if recruits can complete two repetitions over the repetition goal for an exercise for two consecutive workouts, they can increase the weight by five to ten percent for the next strength session."

**Searches:** ['recruit increase weight strength exercise when by how much FM 7-22 progression increase resistance']

**Status:** answered  
**Answer:** For strength training, if recruits can complete two repetitions over the repetition goal for an exercise for two consecutive workouts, they can increase the weight by five to ten percent for the next strength session [fm7-22-2020:p164:para:01].

> **[fm7-22-2020:p164:para:01]** (data/pdf/fm7-22-2020.pdf p164) PHYSICAL TRAINING SESSION 14-15. In untrained recruits, improvement in physical readiness is much greater and more rapid, relatively speaking, than those with advanced levels of fitness. Because of this, low-load and low-volume strength and endurance programs can produce substantial improvements. FSP physical training sessions follow this principle. Leaders can increase volume for trained recruits so long as they continue to follow the RPE guidelines in the FSP weekly templates (see table 14-1). For strength training, if recruits can complete two repetitions over the repetition goal for an exercise for two consecutive workouts, they can increase the weight by five to ten percent for the next strength session.

## q11 (answerable)

**Question:** Which hormone is often called the stress hormone, and what does excessive production of it contribute to?

**Expected:** Cortisol; excess contributes to chronic disease, poor executive cognitive function, and increased susceptibility to injury and infection.

- gold: fm7-22-2020 p104: "One of the hormones released as a result of this protective response is cortisol, often referred to as the “stress hormone.” Excessive production of cortisol contributes to chronic disease, poor executive cognitive function, and increased susceptibility to injury and infection."

**Searches:** ['stress hormone excessive production contributes to cortisol']

**Status:** answered  
**Answer:** Cortisol is often called the stress hormone, and excessive production of it contributes to chronic disease, poor executive cognitive function, and increased susceptibility to injury and infection [fm7-22-2020:p104:para:01].

> **[fm7-22-2020:p104:para:01]** (data/pdf/fm7-22-2020.pdf p104) 9-31. One of the hormones released as a result of this protective response is cortisol, often referred to as the “stress hormone.” Excessive production of cortisol contributes to chronic disease, poor executive cognitive function, and increased susceptibility to injury and infection. When Soldiers are trained to control their activation levels, they can mitigate the negative impact of this physiological reaction. It helps Soldiers if they can understand how they react to stress at its initial onset. Table 9-2 outlines common physiological acute and chronic stress responses. Table 9-2. Physiological changes associated with the stress response Acute, early phase of the stress response (duration in minutes to hours) symptoms: • Increased heart rate • Increased blood pressure

## q12 (answerable)

**Question:** How does the talk test distinguish moderate-intensity from vigorous-intensity aerobic activity?

**Expected:** At moderate intensity a person can talk but not sing; at vigorous intensity they cannot say more than a few words without pausing for a breath.

- gold: hhs-pag-2018 p60: "As a rule of thumb, a person doing moderate-intensity aerobic activity can talk, but not sing, during the activity. A person doing vigorous-intensity activity cannot say more than a few words without pausing for a breath."
- gold: hhs-pag-2018 p71: "As a rule of thumb, a person doing moderate-intensity aerobic activity can talk, but not sing, during the activity. A person doing vigorous-intensity activity cannot say more than a few words without pausing for a breath."

**Searches:** ['talk test moderate-intensity vigorous-intensity aerobic activity speak breathe Physical Activity Guidelines']

**Status:** answered  
**Answer:** A person doing moderate-intensity aerobic activity can talk, but not sing, during the activity; a person doing vigorous-intensity activity cannot say more than a few words without pausing for a breath [hhs-pag-2018:p071:para:02].

> **[hhs-pag-2018:p071:para:02]** (data/pdf/hhs-pag-2018.pdf p71) When using relative intensity, people pay attention to how physical activit y affects their heart rate and breathing. As a rule of thumb, a person doing moderate-intensity aerobic activity can talk, but not sing, during the activity. A person doing vigorous-intensity activity cannot say more than a few words without pausing for a breath.

## q13 (answerable)

**Question:** According to the Physical Activity Guidelines for Americans, how much physical activity should children and adolescents aged 6 through 17 do?

**Expected:** 60 minutes (1 hour) or more of moderate-to-vigorous physical activity daily.

- gold: hhs-pag-2018 p48: "Children and adolescents ages 6 through 17 years should do 60 minutes (1 hour) or more of moderate-to-vigorous physical activity daily"

**Searches:** ['Physical Activity Guidelines for Americans children adolescents 6 through 17 how much physical activity daily 60 minutes']

**Status:** answered  
**Answer:** Children and adolescents ages 6 through 17 years should do 60 minutes (1 hour) or more of moderate-to-vigorous physical activity daily, including vigorous-intensity activity on at least 3 days a week and muscle-strengthening activity on at least 3 days a week [hhs-pag-2018:p048:para:02].

> **[hhs-pag-2018:p048:para:02]** (data/pdf/hhs-pag-2018.pdf p48) Key Guidelines for School-Aged Children and Adolescents It is important to provide young people opportunities and encouragement to participate in physical activities that are appropriate for their age, that are enjoyable, and that offer variety. Children and adolescents ages 6 through 17 years should do 60 minutes (1 hour) or more of moderate-to-vigorous physical activity daily: • Aerobic: Most of the 60 minutes or more per day should be either moderate- or vigorous-intensity aerobic physical activity and should include vigorous-intensity physical activity on at least 3 days a week. • Muscle-strengthening: As part of their 60 minutes or more of daily physical activity, children and adolescents should include muscle-strengthening physical activity on at least 3 days a week.

## q14 (answerable)

**Question:** According to the WHO guidelines, how much physical activity should children and adolescents aged 5–17 do?

**Expected:** At least an average of 60 minutes per day of moderate- to vigorous-intensity, mostly aerobic, physical activity across the week.

- gold: who-pasb-2020 p35: "Children and adolescents should do at least an average of 60 minutes per day of moderate- to vigorous-intensity, mostly aerobic, physical activity, across the week."
- gold: who-pasb-2020 p11: "Children and adolescents should do at least an average of 60 minutes per day of moderate- to vigorous-intensity, mostly aerobic, physical activity, across the week."

**Searches:** ['WHO guidelines children adolescents 5-17 physical activity 60 minutes moderate-to-vigorous daily']

**Status:** answered  
**Answer:** Children and adolescents aged 5–17 should do at least an average of 60 minutes per day of moderate- to vigorous-intensity, mostly aerobic, physical activity, across the week [who-pasb-2020:p011:para:00]. Vigorous-intensity aerobic activities, and activities that strengthen muscle and bone, should be incorporated at least 3 days a week [who-pasb-2020:p011:para:00].

> **[who-pasb-2020:p011:para:00]** (data/pdf/who-pasb-2020.pdf p11) CHILDREN AND ADOLESCENTS (aged 5–17 years) It is recommended that: Children and adolescents should do at least an average of 60 minutes per day of moderate- to vigorous-intensity, mostly aerobic, physical activity, across the week. Strong recommendation, moderate certainty evidence Vigorous-intensity aerobic activities, as well as those that strengthen muscle and bone, should be incorporated at least 3 days a week. Strong recommendation, moderate certainty evidence • Doing some physical activity is better than doing none. • If children and adolescents are not meeting the recommendations, doing some physical activity will benefit their health.

## q15 (answerable)

**Question:** What target did the WHO Global action plan on physical activity 2018–2030 set for physical inactivity?

**Expected:** Reduce physical inactivity by 15% by 2030.

- gold: who-pasb-2020 p83: "Global action plan on physical activity 2018–2030 set a target to reduce physical inactivity by 15% by 2030"
- gold: who-pasb-2020 p10: "Global action plan on physical activity 2018–2030 set a target to reduce physical inactivity by 15% by 2030"
- gold: who-pasb-2020 p25: "to achieve a 15% relative reduction in the global prevalence of physical inactivity in adults and adolescents by 2030"

**Searches:** ['WHO global action plan physical activity 2018 2030 target physical inactivity reduce 15%']

**Status:** answered  
**Answer:** The WHO Global action plan on physical activity 2018–2030 set a target to reduce physical inactivity by 15% by 2030 [who-pasb-2020:p083:para:00].

> **[who-pasb-2020:p083:para:00]** (data/pdf/who-pasb-2020.pdf p83) The WHO Global action plan on physical activity 2018–2030 set a target to reduce physical inactivity by 15% by 2030, and outlined 20 recommended policy actions and interventions (14). These included recommending that all countries implement sustained national public education and awareness campaigns and the integration of physical activity counselling programmes into primary and secondary health care. Other recommendations included the creation of appropriate environments for physical activity, including walking, cycling and wheeling, for all population groups and the provision of more opportunities and programmes for physical activity in schools, workplaces and sports clubs and venues.

## q21 (answerable)

**Question:** What is VO2 max?

**Expected:** The maximal oxygen consumption: the highest amount of oxygen that can be used during maximal aerobic effort.

- gold: fm7-22-2020 p45: "The highest amount of oxygen that can be used during maxima l aerobic effort—endurance training— is called the maximal oxygen consumption, or VO2 max."

**Searches:** ['VO2 max definition aerobic capacity cardiorespiratory fitness']

**Status:** answered  
**Answer:** VO2 max is the maximal oxygen consumption: the highest amount of oxygen that can be used during maximal aerobic effort, measured in mL/kg/min [fm7-22-2020:p045:para:04].

> **[fm7-22-2020:p045:para:04]** (data/pdf/fm7-22-2020.pdf p45) VO2 MAX 4-11. The highest amount of oxygen that can be used during maxima l aerobic effort—endurance training— is called the maximal oxygen consumption, or VO2 max. It is measured as volume (V) in milliliters of oxygen (O2) consumed per kilogram of body weight per minute, abbreviated to m L/kg/min. A recruit who scores black on the OPAT has a predicted VO2 max of 33 mL/kg/min. Over time and with progressive training, that recruit could improve his or her maximal aerobic capacity. Strength training typically results in little or no change in VO2 max unless the Soldier uses longer sessions of circuit -type strength training with shorter rest intervals between exercises.

## q22 (answerable)

**Question:** How much carbohydrate and protein should be consumed after exercise, and how soon?

**Expected:** 50-100 grams of carbohydrate and 15-25 grams of high-quality protein within 30-60 minutes after exercise.

- gold: fm7-22-2020 p89: "It is critical to provide the body with 50 –100 grams of carbohydrate (2 grams of carbohydrates per kilogram of body weight) and 15 –25 grams of high -quality protein (5 –9 grams protein per 100 grams of carbohydrates) within 30 –60 minutes after exercise"

**Searches:** ['post exercise carbohydrate protein how much soon recovery FM 7-22 Physical Activity Guidelines WHO']

**Status:** answered  
**Answer:** 50–100 grams of carbohydrate and 15–25 grams of high-quality protein within 30–60 minutes after exercise [fm7-22-2020:p089:para:01]

> **[fm7-22-2020:p089:para:01]** (data/pdf/fm7-22-2020.pdf p89) 8-36. It is critical to provide the body with 50 –100 grams of carbohydrate (2 grams of carbohydrates per kilogram of body weight) and 15 –25 grams of high -quality protein (5 –9 grams protein per 100 grams of carbohydrates) within 30 –60 minutes after exercise . This protein helps replenish muscle glycogen stores , stimulate muscle protein synthesis, and repair damage caused by intense exercise. If unable to eat a meal within 60 minutes of completing exercise, Soldiers might snack on 8 ounces (1 cup) low-fat chocolate milk, 8 ounces (1 cup) 100-percent fruit juice and a handful of nuts (about 1⁄4 cup), 2 slices whole grain bread with peanut butter and a banana, or 8 ounces (1 cup) low -fat yogurt and a piece of fresh fruit ( for example, 1 medium apple, 1 medium orange, 1 banana).

## q23 (answerable)

**Question:** What are the signs of heatstroke, and how urgent is it?

**Expected:** No sweating, hot dry skin, rapid pulse, rapid breathing, dizziness or confusion, unconsciousness, seizure, or coma; it is a medical emergency (dial 911).

- gold: fm7-22-2020 p164: "Heatstroke (medical emergency, dial 911): no sweating, hot dry skin, rapid pulse, rapid breathing, dizziness or confusion, unconsciousness, seizure, or coma."

**Searches:** ['heatstroke signs urgency FM 7-22 heat illness signs emergency']

**Status:** answered  
**Answer:** Heatstroke signs are no sweating, hot dry skin, rapid pulse, rapid breathing, dizziness or confusion, unconsciousness, seizure, or coma [fm7-22-2020:p164:para:00]. It is a medical emergency; dial 911 [fm7-22-2020:p164:para:00].

> **[fm7-22-2020:p164:para:00]** (data/pdf/fm7-22-2020.pdf p164) • Heat exhaustion (requires medical attention): excessive thirst, fatigue, lack of coordination, increased sweating, cool or wet skin, dizziness, confusion, or combination of symptoms. • Heatstroke (medical emergency, dial 911): no sweating, hot dry skin, rapid pulse, rapid breathing, dizziness or confusion, unconsciousness, seizure, or coma. • Hypothermia: shivering, loss of judgment, slurred speech, drowsiness, or muscle weakness. • Frostbite: white or greyish -yellow skin color, skin that feels unusually firm or waxy, or numbness in body parts exposed to the cold—usually the ears, nose, feet, and hands.

## q24 (answerable)

**Question:** In the Holistic Health and Fitness Schedules chapter, what is the maximum fluid intake per hour during sustained exertion?

**Expected:** No more than 1 1/2 quarts (48 ounces) per hour.

- gold: fm7-22-2020 p163: "Be sure to limit intake to no more than 11⁄2 quarts per hour (48 ounces) during sustained exertion."

**Searches:** ['Holistic Health and Fitness Schedules sustained exertion maximum fluid intake per hour']

**Status:** answered  
**Answer:** 1 1/2 quarts per hour (48 ounces) during sustained exertion [fm7-22-2020:p163:para:03]

> **[fm7-22-2020:p163:para:03]** (data/pdf/fm7-22-2020.pdf p163) HYPONATREMIA It is possible to drink too much water and become overhydrated or hyponatremic. Be sure to limit intake to no more than 11⁄2 quarts per hour (48 ounces) during sustained exertion. Clothing 14-13. Leaders ensure that the clothing is comfortable for the climate and bright or reflective enough for outdoor activity conducted in the dark on roadways or sidewalks. Recruits should never wear rubberized or plastic suits, facemasks , or other restrictive breathing devices during exercise or physical assessments. Personal audio devices and earphones are appropriate for indoor activity . Leaders discourage these devices for outdoor activity where they can reduce situational awareness and increase the risk of injury from other pedestrians and traffic.

## q25 (answerable)

**Question:** What do the guidelines recommend for preschool-aged children (ages 3 through 5)?

**Expected:** They should be physically active throughout the day to enhance growth and development.

- gold: hhs-pag-2018 p47: "Preschool-aged children (ages 3 through 5 years) should be physically active throughout the day to enhance growth and development."

**Searches:** ['preschool-aged children ages 3 through 5 physical activity guidelines 24 hours sedentary sleep WHO HHS FM 7-22']

**Status:** answered  
**Answer:** Preschool-aged children (ages 3 through 5 years) should be physically active throughout the day to enhance growth and development, and adult caregivers should encourage active play that includes a variety of activity types [hhs-pag-2018:p047:para:05]. They should be encouraged to move and engage in active play and structured activities; a reasonable target may be 3 hours per day of activity of all intensities: light, moderate, or vigorous intensity [hhs-pag-2018:p047:para:04].

> **[hhs-pag-2018:p047:para:05]** (data/pdf/hhs-pag-2018.pdf p47) Key Guidelines for Preschool-Aged Children Preschool-aged children (ages 3 through 5 years) should be physically active throughout the day to enhance growth and development. Adult caregivers of preschool-aged children should encourage active play that includes a varie ty of activity types.

> **[hhs-pag-2018:p047:para:04]** (data/pdf/hhs-pag-2018.pdf p47) Preschool-aged children (ages 3 through 5 years) should be encouraged to move and engage in active play as well as in s tructured activities, such as throwing games and bicycle or tricycle riding. To strengthen bones, young children should do activities that involve hopping, skipping, jumping, and tumbling. Although the specific amount of activity needed to improve bone health and avoid excess fat in young children is not well defined, a reasonable target may be 3 hours per day of activity of all intensities: light, moderate, or vigorous intensity. This is the average amount of activity observed among children of this age and is consistent with guidelines from Canada, the United Kingdom, and the Commonwealth of Australia.

## q26 (answerable)

**Question:** What immediate benefits can one bout of moderate-to-vigorous physical activity bring on the same day?

**Expected:** Reduced blood pressure, improved insulin sensitivity, improved sleep, reduced anxiety symptoms, and improved aspects of cognition.

- gold: hhs-pag-2018 p20: "A single session of moderate-to-vigorous physical activity can reduce blood pressure, improve insulin sensitivity, improve sleep, reduce anxiety symptoms, and improve some aspects of cognition on the day that it is performed."

**Searches:** ['same day immediate benefits one bout moderate-to-vigorous physical activity immediate benefits acute effects adults guidelines']

**Status:** answered  
**Answer:** A single session of moderate-to-vigorous physical activity can reduce blood pressure, improve insulin sensitivity, improve sleep, reduce anxiety symptoms, and improve some aspects of cognition on the day it is performed [hhs-pag-2018:p020:para:00].

> **[hhs-pag-2018:p020:para:00]** (data/pdf/hhs-pag-2018.pdf p20) Timing of Benefits A single session of moderate-to-vigorous physical activity can reduce blood pressure, improve insulin sensitivity, improve sleep, reduce anxiety symptoms, and improve some aspects of cognition on the day that it is performed. Most of these improvements become even larger with the regular performance of moderate-to- vigorous physical activity. Other benefits, such as disease risk reduction and improved physical function, accrue within days to weeks after consistently being more physically active. Physical Activity Intensity The Guidelines consider the intensity with which people do physical activity. Some activities are a higher intensity than others because they require more energy to do. For example, a person expends more energy walking briskly than slowly strolling.

## q27 (answerable)

**Question:** How is sedentary behaviour defined?

**Expected:** Time spent sitting, reclining or lying with low energy expenditure while awake.

- gold: who-pasb-2020 p39: "Sedentary behaviour is defined as time spent sitting or lying with low energy expenditure, while awake"
- gold: who-pasb-2020 p25: "sedentary behaviour is defined as any waking behaviour while in a sitting, reclining or lying posture with low energy expenditure"
- gold: who-pasb-2020 p48: "sedentary behaviour is defined as time spent sitting or lying with low energy expenditure, while awake"
- gold: who-pasb-2020 p56: "sedentary behaviour is defined as time spent sitting or lying with low energy expenditure, while awake"
- gold: who-pasb-2020 p61: "sedentary behaviour is defined as time spent sitting or lying with low energy expenditure while awake"
- gold: who-pasb-2020 p68: "Sedentary behaviour is defined as time spent sitting or lying with low energy expenditure, while awake"
- gold: hhs-pag-2018 p45: "sedentary behavior refers to any waking behavior characterized by a low level of energy expenditure (less than or equal to 1.5 METs) while sitting, reclining, or lying."

**Searches:** ['sedentary behaviour defined definition WHO 2020 physical activity sedentary behaviour']

**Status:** answered  
**Answer:** Sedentary behaviour is time spent sitting or lying with low energy expenditure, while awake [who-pasb-2020:p039:para:02].

> **[who-pasb-2020:p039:para:02]** (data/pdf/who-pasb-2020.pdf p39) Strong recommendation, low certainty evidence Available online at https://apps.who.int/iris/bitstream/handle/10665/336657/9789240015111-eng.pdf Sedentary behaviour is defined as time spent sitting or lying with low energy expenditure, while awake, in the context of educational, home, and community settings and transportation. CHILDREN AND ADOLESCENTS (aged 5–17 years) SEDENTARY BEHAVIOUR RECOMMENDATION

## u01 (unanswerable)

**Question:** What physical activity does the WHO recommend for adults recovering from COVID-19?

**Why unanswerable:** The corpus predates or does not address COVID-19; WHO 2020 covers chronic conditions but never mentions COVID.

**Searches:** ['WHO adults recovering from COVID-19 physical activity recommendation', 'WHO adults recovering from COVID-19 physical activity recommendation rehabilitation return to activity', 'WHO adults recovering from COVID-19 rehabilitation physical activity recommendation']

**Status:** abstain  
**Answer:** Không đủ bằng chứng để trả lời.

**Model's raw final call:** `{"answer":"Not enough evidence in the documents.","citations":[]}`

## u02 (unanswerable)

**Question:** How many minutes of aerobic activity per week do the HHS guidelines recommend specifically for adults with type 1 diabetes?

**Why unanswerable:** HHS p83 states type 1 diabetes 'was not addressed for the development of the Guidelines'; the chronic-condition advice covers type 2.

**Searches:** ['HHS guidelines adults with type 1 diabetes aerobic activity minutes per week', 'type 1 diabetes adults aerobic activity minutes per week HHS guideline', 'HHS adults with type 1 diabetes aerobic activity minutes per week']

**Status:** abstain  
**Answer:** Không đủ bằng chứng để trả lời.

**Model's raw final call:** `{"answer":"Not enough evidence in the documents.","citations":[]}`

## u03 (unanswerable)

**Question:** What minimum score in points must a Soldier earn on each ACFT event to pass?

**Why unanswerable:** FM 7-22 names the ACFT 193 times and says Soldiers must 'meet the Army standard' (p176) but contains no scoring scale or point minimums.

**Searches:** ['ACFT minimum score each event pass points Soldier must earn', 'ACFT minimum score each event pass points Army Combat Fitness Test scorecard passing standard', 'ACFT minimum score each event pass points minimum 60 points each event']

**Status:** abstain  
**Answer:** Không đủ bằng chứng để trả lời.

**Model's raw final call:** `{"answer":"Not enough evidence in the documents.","citations":[]}`

